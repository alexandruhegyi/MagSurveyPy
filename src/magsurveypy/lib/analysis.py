from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import math

import numpy as np


def _finite(a):
    x=np.asarray(a,dtype=float)
    return x[np.isfinite(x)]


def robust_sigma(values):
    v=_finite(values)
    if not len(v): return float('nan')
    med=float(np.median(v)); mad=float(np.median(np.abs(v-med)))
    return 1.4826*mad


def infer_units(tags=None, description=None, path=None):
    """Infer magnetic units without silently treating total field as gradient."""
    tags={str(k).lower():str(v) for k,v in (tags or {}).items()}
    joined=' '.join([str(description or ''),str(path or ''),*tags.values()]).lower()
    explicit=(tags.get('units') or tags.get('unit') or '').strip()
    if explicit:
        if 'nt/m' in explicit.lower() or 'nt m-1' in explicit.lower(): return 'nT/m'
        if explicit.lower()=='nt' or 'nanotesla' in explicit.lower(): return 'nT'
    if any(k in joined for k in ('bartington','grad601','grad-01','gradient','bz_grid','nt/m','nt m-1')):
        return 'nT/m'
    if any(k in joined for k in ('total_field','total-field','archaeology anomaly [nt]','field [nt]','caesium','cesium','geometrics')):
        return 'nT'
    return str(tags.get('value_units') or tags.get('units') or 'magnetic units')


def read_raster(path):
    import rasterio
    p=Path(path)
    with rasterio.open(p) as ds:
        a=ds.read(1,masked=True).filled(np.nan).astype(float)
        tags=ds.tags(); desc=(ds.descriptions[0] if ds.descriptions else '') or ''
        return {
            'path':p,'array':a,'transform':ds.transform,'crs':ds.crs,
            'bounds':ds.bounds,'tags':tags,'description':desc,
            'width':ds.width,'height':ds.height,'nodata':ds.nodata,
            'units':infer_units(tags,desc,p),
        }


def raster_statistics(path):
    r=read_raster(path); a=r['array']; v=_finite(a)
    if not len(v): raise ValueError(f'Raster contains no finite values: {path}')
    med=float(np.median(v)); sig=robust_sigma(v)
    tr=r['transform']; cell_x=abs(float(tr.a)); cell_y=abs(float(tr.e))
    return {
        'path':str(r['path']),'units':r['units'],'crs':str(r['crs']),
        'width':int(r['width']),'height':int(r['height']),
        'cell_size_x':cell_x,'cell_size_y':cell_y,
        'finite_cells':int(len(v)),'valid_fraction':float(np.isfinite(a).mean()),
        'min':float(np.min(v)),'max':float(np.max(v)),'mean':float(np.mean(v)),
        'median':med,'std':float(np.std(v)),'robust_sigma':float(sig),
        'p01':float(np.percentile(v,1)),'p05':float(np.percentile(v,5)),
        'p95':float(np.percentile(v,95)),'p99':float(np.percentile(v,99)),
        'p98_abs_about_median':float(np.percentile(np.abs(v-med),98)),
    }


def _fill_nan_for_fft(a):
    from scipy.ndimage import gaussian_filter
    x=np.asarray(a,float); mask=np.isfinite(x)
    if not mask.any(): raise ValueError('No finite values for spectral analysis')
    med=float(np.nanmedian(x)); work=np.where(mask,x,med)
    # Fill holes smoothly only for the diagnostic FFT; quantitative raster is untouched.
    if not mask.all():
        w=gaussian_filter(mask.astype(float),1.2)
        z=gaussian_filter(np.where(mask,work,0.0),1.2)
        fill=np.where(w>1e-6,z/np.maximum(w,1e-6),med)
        work=np.where(mask,work,fill)
    return work-float(np.mean(work))


def spectrum_statistics(path, radial_bins=80):
    r=read_raster(path); x=_fill_nan_for_fft(r['array'])
    ny,nx=x.shape; dx=abs(float(r['transform'].a)); dy=abs(float(r['transform'].e))
    wy=np.hanning(ny)[:,None] if ny>1 else np.ones((ny,1)); wx=np.hanning(nx)[None,:] if nx>1 else np.ones((1,nx))
    F=np.fft.fftshift(np.fft.fft2(x*wy*wx)); P=np.abs(F)**2
    fx=np.fft.fftshift(np.fft.fftfreq(nx,d=dx)); fy=np.fft.fftshift(np.fft.fftfreq(ny,d=dy))
    FX,FY=np.meshgrid(fx,fy); fr=np.sqrt(FX*FX+FY*FY)
    good=(fr>0)&np.isfinite(P)
    if not good.any(): raise ValueError('Insufficient raster size for spectrum')
    edges=np.linspace(0,float(np.nanmax(fr[good])),int(radial_bins)+1); centres=.5*(edges[:-1]+edges[1:])
    ids=np.digitize(fr[good],edges)-1; pv=P[good]
    radial=np.full(len(centres),np.nan)
    for i in range(len(centres)):
        vv=pv[ids==i]
        if len(vv): radial[i]=float(np.median(vv))
    valid=np.isfinite(radial)&(centres>0)
    peak_i=np.nanargmax(radial[valid]) if valid.any() else None
    peak_freq=float(centres[valid][peak_i]) if peak_i is not None else float('nan')
    peak_wavelength=(1.0/peak_freq if np.isfinite(peak_freq) and peak_freq>0 else float('nan'))
    # Orientation diagnostic: power-weighted doubled-angle moment (180-degree symmetry).
    theta=np.arctan2(FY[good],FX[good]); weights=np.maximum(pv,0)
    c=float(np.sum(weights*np.cos(2*theta))/max(np.sum(weights),1e-30)); s=float(np.sum(weights*np.sin(2*theta))/max(np.sum(weights),1e-30))
    anis=float(np.hypot(c,s)); freq_orientation=(0.5*np.degrees(np.arctan2(s,c)))%180.0
    # A stripe in map space is perpendicular to its dominant spectral ridge.
    stripe_orientation=(freq_orientation+90.0)%180.0
    return {
        'path':str(r['path']),'units':r['units'],'cell_size_m':float(np.sqrt(dx*dy)),
        'peak_wavelength_m':float(peak_wavelength),'spectral_anisotropy_0_1':anis,
        'dominant_frequency_orientation_deg_from_east':float(freq_orientation),
        'candidate_map_stripe_orientation_deg_from_east':float(stripe_orientation),
        'radial_frequency_cycles_per_m':centres.tolist(),
        'radial_power':np.where(np.isfinite(radial),radial,np.nan).tolist(),
    }


def _find_column(df,candidates):
    lookup={str(c).strip().lower():c for c in df.columns}
    for name in candidates:
        if name.lower() in lookup: return lookup[name.lower()]
    # substring fallback only for distinctive terms
    for name in candidates:
        for low,orig in lookup.items():
            if len(name)>=4 and name.lower() in low: return orig
    return None


def load_points(path, value_column='auto', line_column='auto', sensor_column='auto'):
    import pandas as pd
    p=Path(path)
    if p.suffix.lower()=='.asc':
        raw=pd.read_csv(p,sep='\t',header=None,comment='#',engine='python')
        if raw.shape[1] < 3: raise ValueError('ASC requires at least x, y, value')
        names=['X','Y','VALUE','SOURCE','SENSOR'][:raw.shape[1]]
        raw=raw.iloc[:,:len(names)]; raw.columns=names
        df=raw
    else:
        try: df=pd.read_csv(p)
        except Exception: df=pd.read_csv(p,sep=r'\s+',engine='python')
    x=_find_column(df,['x','easting','east']); y=_find_column(df,['y','northing','north'])
    if value_column!='auto': value=value_column if value_column in df.columns else _find_column(df,[value_column])
    else: value=_find_column(df,['filtered_value','archaeology_value','magnetic_value','reading','gradient','value','bz','field'])
    if line_column!='auto': line=line_column if line_column in df.columns else _find_column(df,[line_column])
    else: line=_find_column(df,['line','traverse','track','line_id','track_id'])
    if sensor_column!='auto': sensor=sensor_column if sensor_column in df.columns else _find_column(df,[sensor_column])
    else: sensor=_find_column(df,['sensor','sensor_id','channel'])
    source=_find_column(df,['source_file','source','file'])
    if value is None: raise ValueError(f'Cannot identify magnetic-value column in {p.name}. Columns: {list(df.columns)}')
    return {'path':p,'dataframe':df,'x':x,'y':y,'value':value,'line':line,'sensor':sensor,'source':source}


def point_statistics(path, value_column='auto', line_column='auto', sensor_column='auto'):
    import pandas as pd
    obj=load_points(path,value_column,line_column,sensor_column); df=obj['dataframe']; vc=obj['value']
    vals=pd.to_numeric(df[vc],errors='coerce').to_numpy(float); good=np.isfinite(vals); vals=vals[good]
    if not len(vals): raise ValueError('No finite magnetic values in point table')
    out={'path':str(obj['path']),'rows':int(len(df)),'finite_values':int(len(vals)),'value_column':str(vc),'line_column':str(obj['line']) if obj['line'] is not None else None,'sensor_column':str(obj['sensor']) if obj['sensor'] is not None else None,
         'min':float(np.min(vals)),'max':float(np.max(vals)),'mean':float(np.mean(vals)),'median':float(np.median(vals)),'std':float(np.std(vals)),'robust_sigma':float(robust_sigma(vals))}
    if obj['x'] is not None and obj['y'] is not None:
        x=pd.to_numeric(df[obj['x']],errors='coerce').to_numpy(float); y=pd.to_numeric(df[obj['y']],errors='coerce').to_numpy(float); xy=np.isfinite(x)&np.isfinite(y)
        if xy.any(): out['bounds']=[float(np.min(x[xy])),float(np.min(y[xy])),float(np.max(x[xy])),float(np.max(y[xy]))]
    if obj['line'] is not None: out['line_count']=int(df[obj['line']].nunique(dropna=True))
    if obj['sensor'] is not None: out['sensor_count']=int(df[obj['sensor']].nunique(dropna=True))
    return out


def group_statistics(path, group='line', value_column='auto'):
    import pandas as pd
    obj=load_points(path,value_column=value_column); df=obj['dataframe']; gc=obj['line'] if group=='line' else obj['sensor']
    if gc is None: raise ValueError(f'No {group} column detected in {path}')
    vc=obj['value']; work=df[[gc,vc]].copy(); work[vc]=pd.to_numeric(work[vc],errors='coerce'); work=work.dropna()
    rows=[]
    for key,g in work.groupby(gc,sort=False):
        v=g[vc].to_numpy(float); med=float(np.median(v)); rows.append({'group':key,'count':int(len(v)),'mean':float(np.mean(v)),'median':med,'std':float(np.std(v)),'robust_sigma':float(robust_sigma(v)),'min':float(np.min(v)),'max':float(np.max(v))})
    return rows


def write_analysis_dashboard(point_path, raster_path, output_dir, prefix='survey', dpi=240, mspy_credit=False, mspy_credit_position='bottom-left', mspy_credit_size=.10, mspy_credit_alpha=1.0):
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    od=Path(output_dir); od.mkdir(parents=True,exist_ok=True)
    pobj=load_points(point_path) if point_path else None
    r=read_raster(raster_path) if raster_path else None
    pstats=point_statistics(point_path) if point_path else None
    rstats=raster_statistics(raster_path) if raster_path else None
    line_rows=[]; sensor_rows=[]
    if pobj and pobj['line'] is not None:
        line_rows=group_statistics(point_path,'line')
        pd.DataFrame(line_rows).to_csv(od/f'{prefix}_line_statistics.csv',index=False)
    if pobj and pobj['sensor'] is not None:
        sensor_rows=group_statistics(point_path,'sensor')
        pd.DataFrame(sensor_rows).to_csv(od/f'{prefix}_sensor_statistics.csv',index=False)
    spec=None
    if raster_path:
        try: spec=spectrum_statistics(raster_path)
        except Exception: spec=None
    fig,axs=plt.subplots(2,3,figsize=(14,8.5),constrained_layout=True)
    # coverage
    ax=axs[0,0]
    if pobj and pobj['x'] is not None and pobj['y'] is not None:
        df=pobj['dataframe']; x=pd.to_numeric(df[pobj['x']],errors='coerce').to_numpy(float); y=pd.to_numeric(df[pobj['y']],errors='coerce').to_numpy(float); v=pd.to_numeric(df[pobj['value']],errors='coerce').to_numpy(float); g=np.isfinite(x)&np.isfinite(y)&np.isfinite(v); ids=np.flatnonzero(g); step=max(1,int(math.ceil(len(ids)/100000))); ids=ids[::step]
        sc=ax.scatter(x[ids],y[ids],c=v[ids],s=2,cmap='gray_r',rasterized=True); ax.set_aspect('equal',adjustable='box'); ax.set_title('Survey coverage / measurements'); ax.set_xlabel('X'); ax.set_ylabel('Y')
    elif r:
        ax.imshow(r['array'],origin='upper',cmap='gray_r'); ax.set_title('Magnetic raster'); ax.set_axis_off()
    else: ax.text(.5,.5,'No geometry',ha='center',va='center'); ax.set_axis_off()
    # histogram
    ax=axs[0,1]
    vals=None; unit='magnetic units'
    if pobj:
        vals=pd.to_numeric(pobj['dataframe'][pobj['value']],errors='coerce').to_numpy(float); vals=vals[np.isfinite(vals)]
    elif r: vals=_finite(r['array']); unit=r['units']
    if vals is not None and len(vals):
        lo,hi=np.percentile(vals,[.5,99.5]); ax.hist(vals[(vals>=lo)&(vals<=hi)],bins=80); ax.axvline(np.median(vals),lw=1); ax.set_title('Value distribution'); ax.set_xlabel(unit); ax.set_ylabel('Count')
    # line baseline
    ax=axs[0,2]
    if line_rows:
        yy=[q['median'] for q in line_rows]; ax.plot(np.arange(len(yy)),yy,'o-',ms=2,lw=.8); ax.set_title('Traverse / line medians'); ax.set_xlabel('Line sequence'); ax.set_ylabel('Median')
    else: ax.text(.5,.5,'No line groups detected',ha='center',va='center'); ax.set_axis_off()
    # line noise
    ax=axs[1,0]
    if line_rows:
        yy=[q['robust_sigma'] for q in line_rows]; ax.plot(np.arange(len(yy)),yy,lw=.8); ax.set_title('Line robust noise / variability'); ax.set_xlabel('Line sequence'); ax.set_ylabel('Robust σ')
    elif sensor_rows:
        names=[str(q['group']) for q in sensor_rows]; yy=[q['robust_sigma'] for q in sensor_rows]; ax.bar(names,yy); ax.set_title('Sensor robust variability'); ax.set_ylabel('Robust σ')
    else: ax.text(.5,.5,'No grouped QC available',ha='center',va='center'); ax.set_axis_off()
    # sensor baselines
    ax=axs[1,1]
    if sensor_rows:
        names=[str(q['group']) for q in sensor_rows]; yy=[q['median'] for q in sensor_rows]; ax.bar(names,yy); ax.set_title('Sensor/channel medians'); ax.set_xlabel('Sensor'); ax.set_ylabel('Median')
    else: ax.text(.5,.5,'Single sensor or no sensor column',ha='center',va='center'); ax.set_axis_off()
    # spectrum
    ax=axs[1,2]
    if spec:
        f=np.asarray(spec['radial_frequency_cycles_per_m'],float); p=np.asarray(spec['radial_power'],float); g=(f>0)&np.isfinite(p)&(p>0); ax.loglog(1.0/f[g],p[g]); ax.set_title(f"Radial spectrum\nstripe candidate {spec['candidate_map_stripe_orientation_deg_from_east']:.1f}°"); ax.set_xlabel('Wavelength (m)'); ax.set_ylabel('Median power'); ax.invert_xaxis()
    else: ax.text(.5,.5,'No raster spectrum available',ha='center',va='center'); ax.set_axis_off()
    if mspy_credit:
        try:
            logo=Path(__file__).resolve().parent.parent/'assets'/'magsurveypy_logo.png'; arr=plt.imread(logo); hh,ww=arr.shape[:2]; fw,fh=fig.get_size_inches(); width=max(.035,min(.28,float(mspy_credit_size)*1.45)); height=width*(hh/ww)*(fw/fh); pos=str(mspy_credit_position); x=.008 if pos.endswith('left') else (.5-width/2 if pos.endswith('center') else .992-width); iax=fig.add_axes([x,.006,width,height],zorder=100); iax.imshow(arr,alpha=max(0,min(1,float(mspy_credit_alpha)))); iax.set_axis_off()
        except Exception:
            pass
    fp=od/f'{prefix}_survey_dashboard.png'; fig.savefig(fp,dpi=dpi,bbox_inches='tight'); plt.close(fig)
    report={'point_statistics':pstats,'raster_statistics':rstats,'spectrum':spec,'line_statistics_csv':str(od/f'{prefix}_line_statistics.csv') if line_rows else None,'sensor_statistics_csv':str(od/f'{prefix}_sensor_statistics.csv') if sensor_rows else None,'dashboard':str(fp)}
    (od/f'{prefix}_analysis.json').write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    return report
