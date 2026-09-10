from __future__ import annotations
from pathlib import Path
import json
import numpy as np

from .analysis import load_points, robust_sigma


def _centre(v,mode,sigma=4.5):
    x=np.asarray(v,float); good=np.isfinite(x)
    if not good.any(): return 0.0
    z=x[good]
    if mode=='mean': return float(np.mean(z))
    if mode=='median': return float(np.median(z))
    if mode=='robust':
        med=float(np.median(z)); rs=robust_sigma(z)
        if not np.isfinite(rs) or rs<=0: return med
        keep=np.abs(z-med)<=float(sigma)*rs
        return float(np.mean(z[keep])) if keep.any() else med
    return 0.0


def filter_observations(input_path, output_dir, *, value_column='auto', line_column='auto', sensor_column='auto',
                        despike_sigma=0.0, line_zero='off', line_detrend='off', center='off', robust_sigma_clip=4.5,
                        prefix=None):
    """Filter normalized point observations without altering the source file.

    Designed for transparent pre-grid QC. It intentionally does not interpolate,
    smooth spatially, or mutate proprietary raw instrument files.
    """
    import pandas as pd
    from scipy.stats import linregress
    obj=load_points(input_path,value_column,line_column,sensor_column); df=obj['dataframe'].copy(); vc=obj['value']; lc=obj['line']
    vals=pd.to_numeric(df[vc],errors='coerce').to_numpy(float); original=vals.copy(); removed=np.zeros_like(vals,float)
    valid=np.isfinite(vals); despike_mask=np.zeros(len(vals),bool)
    if despike_sigma and float(despike_sigma)>0:
        if lc is not None:
            groups=df[lc].astype(str).fillna('')
            for _,idx in groups.groupby(groups).groups.items():
                ii=np.asarray(list(idx),int); z=vals[ii]; med=np.nanmedian(z); rs=robust_sigma(z)
                if np.isfinite(rs) and rs>0: despike_mask[ii]=np.abs(z-med)>float(despike_sigma)*rs
        else:
            med=np.nanmedian(vals); rs=robust_sigma(vals)
            if np.isfinite(rs) and rs>0: despike_mask=np.abs(vals-med)>float(despike_sigma)*rs
        vals[despike_mask]=np.nan
    line_offsets=[]
    if (line_zero!='off' or line_detrend!='off') and lc is None:
        raise ValueError('Line/traverse filtering requested but no line column was detected. Supply --line-column explicitly or use survey-level instrument processing.')
    if lc is not None and (line_zero!='off' or line_detrend!='off'):
        groups=df.groupby(lc,sort=False,dropna=False).groups
        xcol=obj['x']; ycol=obj['y']
        for key,idx in groups.items():
            ii=np.asarray(list(idx),int); z=vals[ii].copy(); baseline=0.0; slope=0.0
            if line_detrend=='linear':
                if xcol is not None and ycol is not None:
                    xx=pd.to_numeric(df.loc[ii,xcol],errors='coerce').to_numpy(float); yy=pd.to_numeric(df.loc[ii,ycol],errors='coerce').to_numpy(float)
                    # Use cumulative distance in acquisition-table order; no geometry is changed.
                    ds=np.sqrt(np.diff(xx)**2+np.diff(yy)**2); t=np.r_[0,np.nancumsum(np.where(np.isfinite(ds),ds,0.0))]
                else: t=np.arange(len(ii),dtype=float)
                g=np.isfinite(t)&np.isfinite(z)
                if g.sum()>=3:
                    lr=linregress(t[g],z[g]); trend=lr.intercept+lr.slope*t; z=z-trend+float(np.nanmedian(trend[g])); slope=float(lr.slope)
            if line_zero!='off':
                baseline=_centre(z,line_zero,robust_sigma_clip); z=z-baseline
            vals[ii]=z; line_offsets.append({'line':str(key),'count':int(np.isfinite(z).sum()),'zero_mode':line_zero,'baseline_removed':float(baseline),'linear_slope_removed_per_distance':float(slope)})
    global_center=0.0
    if center!='off': global_center=_centre(vals,center,robust_sigma_clip); vals=vals-global_center
    removed=np.where(np.isfinite(original)&np.isfinite(vals),original-vals,np.nan)
    out=df.copy(); out['ORIGINAL_VALUE']=original; out['FILTERED_VALUE']=vals; out['REMOVED_COMPONENT']=removed; out['DESPIKE_REMOVED']=despike_mask
    od=Path(output_dir); od.mkdir(parents=True,exist_ok=True); pref=prefix or Path(input_path).stem
    csvp=od/f'{pref}_filtered_observations.csv'; out.to_csv(csvp,index=False)
    # Write a normalized five-column ASC for direct use by MagSurveyPy interpolation.
    xcol=obj['x']; ycol=obj['y']; sourcecol=obj['source']; sensorcol=obj['sensor']
    ascp=None
    if xcol is not None and ycol is not None:
        x=pd.to_numeric(df[xcol],errors='coerce').to_numpy(float); y=pd.to_numeric(df[ycol],errors='coerce').to_numpy(float)
        source=(df[sourcecol].astype(str).to_numpy() if sourcecol is not None else np.array([Path(input_path).name]*len(df),object))
        sensor=(pd.to_numeric(df[sensorcol],errors='coerce').fillna(0).astype(int).to_numpy() if sensorcol is not None else np.zeros(len(df),int))
        g=np.isfinite(x)&np.isfinite(y)&np.isfinite(vals)
        ascp=od/f'{pref}_filtered_observations.asc'
        with ascp.open('w',encoding='utf-8') as f:
            for xx,yy,vv,ss,se in zip(x[g],y[g],vals[g],source[g],sensor[g]): f.write(f'{xx:.6f}\t{yy:.6f}\t{vv:.9g}\t{ss}\t{int(se)}\n')
    report={'input':str(input_path),'output_csv':str(csvp),'output_asc':str(ascp) if ascp else None,'rows':int(len(df)),'finite_output':int(np.isfinite(vals).sum()),'despikes_removed':int(despike_mask.sum()),'line_zero':line_zero,'line_detrend':line_detrend,'global_center':center,'global_center_removed':float(global_center),'line_corrections':line_offsets,'scientific_policy':'Source observations are never overwritten. Filtering is explicit and auditable; spatial interpolation is not performed here.'}
    rp=od/f'{pref}_filter_report.json'; rp.write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report
