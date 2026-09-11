from __future__ import annotations
from pathlib import Path
import json
import numpy as np

from .analysis import read_raster, raster_statistics, spectrum_statistics, load_points, group_statistics, infer_units


def write_recipe_template(path, project='Site', preset='analysis'):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    if preset=='comparison':
        panels=[
            {'type':'raster','source':'INTERPOLATED','title':'Interpolated','display_range':10,'cmap':'gray_r','colorbar':True},
            {'type':'raster','source':'CLEAN','title':'Cleaned','display_range':10,'cmap':'gray_r','colorbar':True},
            {'type':'difference','source':'INTERPOLATED','source2':'CLEAN','title':'Difference','cmap':'RdBu_r','colorbar':True},
            {'type':'histogram','source':'INTERPOLATED','title':'Value distribution'},
        ]
    elif preset=='publication':
        panels=[
            {'type':'raster','source':'INTERPOLATED','title':'Magnetic anomaly','display_range':10,'cmap':'gray_r','colorbar':True},
            {'type':'spectrum','source':'INTERPOLATED','title':'Radial power spectrum'},
            {'type':'line-summary','title':'Traverse medians'},
            {'type':'sensor-summary','title':'Sensor/channel comparison'},
        ]
    else:
        panels=[
            {'type':'raster','source':'INTERPOLATED','title':'Magnetic raster','display_range':10,'cmap':'gray_r','colorbar':True},
            {'type':'histogram','source':'INTERPOLATED','title':'Distribution'},
            {'type':'spectrum','source':'INTERPOLATED','title':'Spatial spectrum'},
            {'type':'line-summary','title':'Traverse QC'},
            {'type':'sensor-summary','title':'Sensor QC'},
            {'type':'text','title':'Notes','text':'Replace this text with interpretation notes or a figure caption draft.'},
        ]
    recipe={'project':project,'title':f'{project} — magnetic survey analysis','layout':{'rows':2,'cols':3 if len(panels)>4 else 2,'width':14,'height':8.5,'dpi':300,'wspace':0.38,'hspace':0.30},'shared':{'font_size':9,'title_size':12,'axis_label_size':8,'tick_label_size':7,'colorbar_label_size':8,'colorbar_tick_size':7,'display_contrast':1.0,'display_brightness':1.0,'display_gamma':1.0,'display_saturation':1.0,'credit_size':.10,'credit_position':'bottom-left','credit_alpha':1.0,'credits':False},'panels':panels}
    p.write_text(json.dumps(recipe,indent=2),encoding='utf-8'); return p



def _display_cmap(cmap='gray_r', contrast=1.0, brightness=1.0, gamma=1.0, saturation=1.0):
    """Display-only colormap tone adjustment; quantitative values stay unchanged."""
    import matplotlib as mpl
    from matplotlib.colors import ListedColormap
    try: base=mpl.colormaps.get_cmap(cmap)
    except Exception: base=mpl.colormaps.get_cmap('gray_r')
    rgba=np.asarray(base(np.linspace(0.0,1.0,1024)),float).copy(); rgb=np.clip(rgba[:,:3],0,1)
    c=max(0.0,float(contrast)); b=max(0.0,float(brightness)); g=max(1e-6,float(gamma)); sat=max(0.0,float(saturation))
    rgb=np.power(rgb,1.0/g); rgb=(rgb-.5)*c+.5; rgb*=b
    lum=rgb[:,0]*.2126+rgb[:,1]*.7152+rgb[:,2]*.0722; rgb=lum[:,None]+sat*(rgb-lum[:,None]); rgba[:,:3]=np.clip(rgb,0,1)
    return ListedColormap(rgba,name=f'mspy_recipe_{getattr(base,"name","cmap")}')


def _format_cb_tick(v):
    v=float(v)
    if abs(v) < 1e-12: v=0.0
    if abs(v-round(v)) <= max(1e-10,abs(v)*1e-10): return str(int(round(v)))
    return f'{v:.3f}'.rstrip('0').rstrip('.')


def _pin_colorbar_endpoints(cb,im):
    try:
        from matplotlib.ticker import MaxNLocator,FuncFormatter
        lo=float(im.norm.vmin); hi=float(im.norm.vmax)
        if not (np.isfinite(lo) and np.isfinite(hi) and hi>lo): return
        span=hi-lo; vals=[float(x) for x in MaxNLocator(nbins=5,steps=[1,2,2.5,5,10],min_n_ticks=3).tick_values(lo,hi) if lo<float(x)<hi]
        guard=max(abs(span)*.045,1e-12); vals=[x for x in vals if x-lo>guard and hi-x>guard]
        ticks=[lo,*vals,hi]; clean=[]; tol=max(abs(span)*1e-10,1e-12)
        for x in ticks:
            if not clean or abs(x-clean[-1])>tol: clean.append(x)
        cb.set_ticks(clean); axis=cb.ax.yaxis if getattr(cb,'orientation','vertical')=='vertical' else cb.ax.xaxis; axis.set_major_formatter(FuncFormatter(lambda x,pos:_format_cb_tick(x))); cb.update_ticks()
    except Exception: pass

def _adaptive_colorbar_ticks(cb,im,tick_fontsize=7.0):
    try:
        from matplotlib.ticker import MaxNLocator,FuncFormatter
        fig=cb.ax.figure; fig.canvas.draw(); lo=float(im.norm.vmin); hi=float(im.norm.vmax)
        if not (np.isfinite(lo) and np.isfinite(hi) and hi>lo): return
        orient=getattr(cb,'orientation','vertical'); bbox=cb.ax.get_window_extent(renderer=fig.canvas.get_renderer()); long_px=float(bbox.width if orient=='horizontal' else bbox.height)
        max_chars=max(len(_format_cb_tick(lo)),len(_format_cb_tick(hi))); fs=max(5.0,float(tick_fontsize)); label_px=max(18.0,max_chars*.58*fs*fig.dpi/72.0)
        max_ticks=max(2,min(6,int(long_px/max(label_px*1.35,1.0)))) if orient=='horizontal' else max(3,min(6,int(long_px/max(fs*fig.dpi/72.0*2.1,1.0))))
        vals=[float(x) for x in MaxNLocator(nbins=max(1,max_ticks-1),steps=[1,2,2.5,5,10],min_n_ticks=2).tick_values(lo,hi) if lo<float(x)<hi]
        guard=max(abs(hi-lo)*.06,1e-12); vals=[x for x in vals if x-lo>guard and hi-x>guard]
        if len(vals)>max_ticks-2:
            vals=[] if max_ticks<=2 else [vals[i] for i in np.linspace(0,len(vals)-1,max_ticks-2,dtype=int)]
        ticks=[lo,*vals,hi]; clean=[]; tol=max(abs(hi-lo)*1e-10,1e-12)
        for x in ticks:
            if not clean or abs(x-clean[-1])>tol: clean.append(x)
        cb.set_ticks(clean); axis=cb.ax.xaxis if orient=='horizontal' else cb.ax.yaxis; fmt=FuncFormatter(lambda x,pos:_format_cb_tick(x)); cb.formatter=fmt; axis.set_major_formatter(fmt); cb.update_ticks(); axis.get_offset_text().set_visible(False)
    except Exception: _pin_colorbar_endpoints(cb,im)


def _limits(a,display_range=None,display_min=None,display_max=None):
    v=a[np.isfinite(a)]; med=float(np.median(v)) if len(v) else 0.0
    if display_min is not None or display_max is not None:
        if display_min is None or display_max is None: raise ValueError('display_min and display_max must be supplied together')
        lo=float(display_min); hi=float(display_max)
        if not (np.isfinite(lo) and np.isfinite(hi) and hi>lo): raise ValueError('display_max must be greater than display_min')
        return lo,hi
    if display_range is not None: lim=abs(float(display_range))
    else: lim=float(np.percentile(np.abs(v-med),98.5)) if len(v) else 1.0
    return med-lim,med+lim


def _recipe_colorbar(fig,ax,im,label,p,shared):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    pos=str(p.get('colorbar_position','right')).lower(); divider=make_axes_locatable(ax)
    thick=float(p.get('colorbar_thickness',shared.get('colorbar_thickness',.10)))
    if pos=='bottom': cax=divider.append_axes('bottom',size=thick,pad=float(p.get('colorbar_pad',.48))); cb=fig.colorbar(im,cax=cax,orientation='horizontal')
    else: cax=divider.append_axes('right',size=thick,pad=float(p.get('colorbar_pad',.12))); cb=fig.colorbar(im,cax=cax,orientation='vertical')
    cb.set_label(str(label),fontsize=float(p.get('colorbar_label_size',shared.get('colorbar_label_size',8))))
    cb.ax.tick_params(labelsize=float(p.get('colorbar_tick_size',shared.get('colorbar_tick_size',7))))
    cb.outline.set_linewidth(.6); _adaptive_colorbar_ticks(cb,im,float(p.get('colorbar_tick_size',shared.get('colorbar_tick_size',7)))); return cb


def _recipe_scale_bar(ax,bounds,crs,p,shared):
    if not p.get('scale_bar',False) or crs is None: return
    try:
        from pyproj import CRS,Geod
        import matplotlib.patches as patches, math
        cc=CRS.from_user_input(crs); width=abs(float(bounds.right-bounds.left)); midy=(bounds.bottom+bounds.top)/2
        if cc.is_geographic: _,_,wm=Geod(ellps='WGS84').inv(bounds.left,midy,bounds.right,midy); wm=abs(wm)
        else:
            fac=float(cc.axis_info[0].unit_conversion_factor or 1.0) if cc.axis_info else 1.0; wm=width*fac
        if wm<=0:return
        n=max(1,min(8,int(p.get('scale_bar_segments',4)))); target=wm*.32/n; exp=math.floor(math.log10(max(target,1e-9))); vals=[m*10**e for e in range(exp-2,exp+3) for m in (1,2,2.5,5,10)]; segm=min(vals,key=lambda v:abs(v-target)); total=segm*n; frac=min(.50,max(.16,total/wm)); pos=str(p.get('scale_bar_position','inside-bottom-left')); right='right' in pos; center='center' in pos; top='top' in pos; outside=pos.startswith('outside-'); x0=(.5-frac/2 if center else (.965-frac if right else .035)); y0=(1.075 if outside else .935) if top else (-.095 if outside else .05); extra=.13 if outside and (not top) and p.get('colorbar',True) and str(p.get('colorbar_position','right')).lower()=='bottom' else 0.0; y0-=extra; bh=.011; box=bool(p.get('scale_bar_box',True)); alpha=float(p.get('scale_bar_box_alpha',.86)); fs=float(p.get('scale_bar_font_size',6.2)); style=str(p.get('scale_bar_style','blocks'))
        boxp=None
        if box: boxp=patches.FancyBboxPatch((x0-.015,y0-.032),frac+.03,bh+.048,boxstyle='round,pad=.004',transform=ax.transAxes,facecolor='white',edgecolor='.25',lw=.35,alpha=alpha,zorder=30,clip_on=not outside); ax.add_patch(boxp)
        ss=frac/n
        if style=='blocks':
            for i in range(n): ax.add_patch(patches.Rectangle((x0+i*ss,y0),ss,bh,transform=ax.transAxes,facecolor=('.1' if i%2==0 else 'white'),edgecolor='.1',lw=.5,zorder=31,clip_on=not outside))
        else: ax.plot([x0,x0+frac],[y0+bh/2,y0+bh/2],transform=ax.transAxes,color='.1',lw=1.1,zorder=31,clip_on=not outside)
        usekm=total>=2000
        for i in range(n+1):
            xx=x0+i*ss; ax.plot([xx,xx],[y0,y0+bh*1.3],transform=ax.transAxes,color='.1',lw=.55,zorder=32,clip_on=not outside); val=segm*i/1000 if usekm else segm*i; txt=f'{val:g}'+((' km' if usekm else ' m') if i==n else ''); ha='left' if i==0 else ('right' if i==n else 'center'); t=ax.text(xx,y0-.012,txt,transform=ax.transAxes,ha=ha,va='top',fontsize=fs,zorder=33,clip_on=False); t.set_clip_path(boxp) if boxp is not None and not outside else None
    except Exception: return


def _recipe_north(ax,p):
    if not p.get('north_arrow',False): return
    try:
        from PIL import Image
        from matplotlib.offsetbox import OffsetImage,AnnotationBbox
        path=Path(__file__).resolve().parent.parent/'assets'/'north_arrow.png'; arr=Image.open(path).convert('RGBA'); pos=str(p.get('north_position','inside-top-right')); outside=pos.startswith('outside-'); top='top' in pos; right='right' in pos; left='left' in pos; x=.965 if right else (.035 if left else .5); y=(1.025 if outside else .965) if top else (-.025 if outside else .035); align=(1 if right else (0 if left else .5),(0 if top else 1) if outside else (1 if top else 0)); oi=OffsetImage(arr,zoom=float(p.get('north_size',.10))); frame=bool(p.get('north_box',True)); ab=AnnotationBbox(oi,(x,y),xycoords='axes fraction',box_alignment=align,frameon=frame,bboxprops=dict(boxstyle='round,pad=.12',facecolor='white',edgecolor='none',alpha=float(p.get('north_box_alpha',.56))),annotation_clip=not outside,zorder=40); ax.add_artist(ab)
    except Exception: return


def build_recipe_figure(recipe_path, output_path, *, resolve_raster, resolve_points, dpi=None):
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm
    recipe=json.loads(Path(recipe_path).read_text(encoding='utf-8'))
    layout=recipe.get('layout',{}); shared=recipe.get('shared',{}); panels=list(recipe.get('panels',[])); rows=int(layout.get('rows',2)); cols=int(layout.get('cols',2))
    if len(panels)>rows*cols: rows=int(np.ceil(len(panels)/cols))
    fig,axs=plt.subplots(rows,cols,figsize=(float(layout.get('width',6.5*cols)),float(layout.get('height',4.8*rows))),squeeze=False,constrained_layout=False)
    fig.subplots_adjust(left=float(layout.get('left',0.065)),right=float(layout.get('right',0.97)),bottom=float(layout.get('bottom',0.085)),top=float(layout.get('top',0.90)),wspace=float(layout.get('wspace',0.38)),hspace=float(layout.get('hspace',0.30)))
    fig.suptitle(str(recipe.get('title','MagSurveyPy figure')),fontsize=float(shared.get('title_size',12)))
    for i,ax in enumerate(axs.flat):
        if i>=len(panels): ax.set_axis_off(); continue
        p=panels[i]; typ=str(p.get('type','raster')).lower(); title=str(p.get('title',''))
        try:
            if typ in {'raster','difference'}:
                r1=read_raster(resolve_raster(p.get('source'))); arr=r1['array']; units=r1['units']
                if typ=='difference':
                    r2=read_raster(resolve_raster(p.get('source2')))
                    if r2['array'].shape!=arr.shape: raise ValueError('difference panels require same raster shape/grid')
                    arr=arr-r2['array']; units=r1['units']; v=arr[np.isfinite(arr)]; lim=float(np.percentile(np.abs(v),98.5)) if len(v) else 1.0; vmin,vmax=-lim,lim
                else: vmin,vmax=_limits(arr,p.get('display_range'),p.get('display_min'),p.get('display_max'))
                b=r1['bounds']; dcmap=_display_cmap(p.get('cmap','gray_r'),p.get('display_contrast',shared.get('display_contrast',1.0)),p.get('display_brightness',shared.get('display_brightness',1.0)),p.get('display_gamma',shared.get('display_gamma',1.0)),p.get('display_saturation',shared.get('display_saturation',1.0))); im=ax.imshow(arr,origin='upper',extent=(b.left,b.right,b.bottom,b.top),cmap=dcmap,vmin=vmin,vmax=vmax,interpolation='nearest'); ax.set_aspect('equal',adjustable='box'); ax.set_xlabel(p.get('xlabel','Easting'),fontsize=float(p.get('axis_label_size',shared.get('axis_label_size',8)))); ax.set_ylabel(p.get('ylabel','Northing'),fontsize=float(p.get('axis_label_size',shared.get('axis_label_size',8))))
                try:
                    from matplotlib.ticker import FuncFormatter,MaxNLocator
                    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:.0f}')); ax.yaxis.set_major_formatter(FuncFormatter(lambda y,pos:f'{y:.0f}')); ax.xaxis.set_major_locator(MaxNLocator(nbins=6)); ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
                    for lab in ax.get_yticklabels(): lab.set_rotation(90); lab.set_va('center'); lab.set_ha('center')
                    ax.tick_params(axis='both',labelsize=float(p.get('tick_label_size',shared.get('tick_label_size',7)))); ax.tick_params(axis='y',pad=9)
                except Exception: pass
                if p.get('colorbar',True):
                    unit_raw=p.get('magnetic_unit','auto'); unit=units if unit_raw in (None,'auto','AUTO') else str(unit_raw); label=str(p.get('colorbar_label',f"{p.get('magnetic_label','Magnetic value')} ({unit})" if unit else p.get('magnetic_label','Magnetic value'))); _recipe_colorbar(fig,ax,im,label,p,shared)
                _recipe_scale_bar(ax,b,r1.get('crs'),p,shared); _recipe_north(ax,p)
            elif typ=='histogram':
                r=read_raster(resolve_raster(p.get('source'))); v=r['array'][np.isfinite(r['array'])]; lo,hi=np.percentile(v,[.5,99.5]); ax.hist(v[(v>=lo)&(v<=hi)],bins=int(p.get('bins',80))); ax.axvline(np.median(v),lw=1); ax.set_xlabel(r['units']); ax.set_ylabel('Count')
            elif typ=='spectrum':
                s=spectrum_statistics(resolve_raster(p.get('source'))); f=np.asarray(s['radial_frequency_cycles_per_m']); z=np.asarray(s['radial_power']); g=(f>0)&np.isfinite(z)&(z>0); ax.loglog(1.0/f[g],z[g]); ax.invert_xaxis(); ax.set_xlabel('Wavelength (m)'); ax.set_ylabel('Median power'); ax.text(.02,.02,f"Stripe candidate: {s['candidate_map_stripe_orientation_deg_from_east']:.1f}°\nAnisotropy: {s['spectral_anisotropy_0_1']:.2f}",transform=ax.transAxes,fontsize=8,va='bottom')
            elif typ in {'line-summary','sensor-summary'}:
                pp=resolve_points(); grp='line' if typ=='line-summary' else 'sensor'; rowsg=group_statistics(pp,grp)
                if not rowsg: raise ValueError(f'no {grp} groups')
                x=np.arange(len(rowsg)); med=[q['median'] for q in rowsg]; rs=[q['robust_sigma'] for q in rowsg]; ax.plot(x,med,'o-',ms=2,lw=.8,label='median'); ax2=ax.twinx(); ax2.plot(x,rs,lw=.7,alpha=.65,label='robust σ'); ax.set_xlabel('Sequence' if grp=='line' else 'Sensor/channel'); ax.set_ylabel('Median'); ax2.set_ylabel('Robust σ')
            elif typ=='image':
                img=plt.imread(Path(p['path']).expanduser()); ax.imshow(img); ax.set_axis_off()
            elif typ=='text':
                ax.text(.02,.98,str(p.get('text','')),ha='left',va='top',wrap=True,transform=ax.transAxes); ax.set_axis_off()
            else: raise ValueError(f'unknown panel type: {typ}')
            if title: ax.set_title(title,fontsize=float(p.get('title_size',shared.get('panel_title_size',10))))
        except Exception as exc:
            ax.text(.5,.5,f'{typ} panel unavailable\n{exc}',ha='center',va='center',wrap=True); ax.set_axis_off();
            if title: ax.set_title(title,fontsize=float(p.get('title_size',shared.get('panel_title_size',10))))
    if shared.get('credits',False):
        try:
            logo=Path(__file__).resolve().parent.parent/'assets'/'magsurveypy_logo.png'; arr=plt.imread(logo); hh,ww=arr.shape[:2]; fw,fh=fig.get_size_inches(); width=max(.035,min(.28,float(shared.get('credit_size',.10))*1.45)); height=width*(hh/ww)*(fw/fh); pos=str(shared.get('credit_position','bottom-left')); x=.008 if pos.endswith('left') else (.5-width/2 if pos.endswith('center') else .992-width); iax=fig.add_axes([x,.006,width,height],zorder=100); iax.imshow(arr,alpha=max(0,min(1,float(shared.get('credit_alpha',1.0))))); iax.set_axis_off()
        except Exception:
            pass
    out=Path(output_path); out.parent.mkdir(parents=True,exist_ok=True); fig.savefig(out,dpi=int(dpi or layout.get('dpi',300)),bbox_inches='tight',pad_inches=.06); plt.close(fig); return out
