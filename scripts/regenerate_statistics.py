from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT=Path('Experiments1/data/final_model_comparison_metrics')
SRC=ROOT/'final_row_level_metric_source.csv'
B_BOOT=10000
B_SIGN=20000
SEED=20260915
rng=np.random.default_rng(SEED)
df=pd.read_csv(SRC)

# Point estimates and percentile CIs use line identifiers as the resampling unit.
def metrics(frame, idx=None):
    if idx is None:
        ce=frame.char_edits.to_numpy(float); cr=frame.char_ref_len.to_numpy(float)
        we=frame.word_edits.to_numpy(float); wr=frame.word_ref_len.to_numpy(float)
        ex=frame.exact.to_numpy(float)
        return np.array([(ce/cr).mean(), (we/wr).mean(), ex.mean(), ce.sum()/cr.sum(), we.sum()/wr.sum()])
    ce=frame.char_edits.to_numpy(float); cr=frame.char_ref_len.to_numpy(float)
    we=frame.word_edits.to_numpy(float); wr=frame.word_ref_len.to_numpy(float)
    ex=frame.exact.to_numpy(float)
    return np.column_stack(((ce[idx]/cr[idx]).mean(1), (we[idx]/wr[idx]).mean(1), ex[idx].mean(1), ce[idx].sum(1)/cr[idx].sum(1), we[idx].sum(1)/wr[idx].sum(1)))

def boot(frame):
    n=len(frame); draws=[]
    for _ in range(0,B_BOOT,100):
        idx=rng.integers(0,n,size=(min(100,B_BOOT-len(draws)*100),n))
        draws.append(metrics(frame,idx))
    x=np.vstack(draws)
    point=metrics(frame)
    return point,np.quantile(x,.025,axis=0),np.quantile(x,.975,axis=0)

ci=[]
for (model,split),g in df.groupby(['model','split'],sort=True):
    point,lo,hi=boot(g)
    for name,i in [('cer',0),('wer',1),('exact_match',2),('micro_cer',3),('micro_wer',4)]:
        ci.append(dict(model=model,split=split,metric=name,point=point[i],ci_low=lo[i],ci_high=hi[i],n=len(g),bootstrap_replicates=B_BOOT,seed=SEED))
ci=pd.DataFrame(ci)
ci.to_csv(ROOT/'bootstrap_confidence_intervals_regenerated.csv',index=False)

pairs=[
 ('printed','Qwen3-VL-8B','Qwen3-VL-32B'),('handwritten','GPT-5.4 mini','Gemini Flash'),
 ('handwritten','Qwen3-VL-8B','Qwen3-VL-32B'),('handwritten','Qwen2.5-VL-72B','Qwen3-VL-8B'),
 ('printed','AIN 7B','Qwen3-VL-8B'),('printed','Qwen3-VL-8B','GPT-5.4 mini')]
rows=[]
for split,a,b in pairs:
    x=df[(df.split==split)&(df.model==a)].set_index('id')
    y=df[(df.split==split)&(df.model==b)].set_index('id')
    ids=x.index.intersection(y.index)
    x=x.loc[ids]; y=y.loc[ids]
    values=[('cer',x.char_edits/x.char_ref_len,y.char_edits/y.char_ref_len),('wer',x.word_edits/x.word_ref_len,y.word_edits/y.word_ref_len),('exact_match',x.exact,y.exact)]
    for metric,va,vb in values:
        d=(va-vb).to_numpy(float); n=len(d); point=d.mean(); draws=[]
        for i in range(0,B_BOOT,100):
            idx=rng.integers(0,n,size=(min(100,B_BOOT-i),n))
            draws.append(d[idx].mean(1))
        bd=np.concatenate(draws)
        extreme=0
        for i in range(0,B_SIGN,100):
            signs=rng.choice(np.array([-1.0,1.0]),size=(min(100,B_SIGN-i),n))
            extreme += np.count_nonzero(np.abs((signs*d).mean(1))>=abs(point))
        p=(1+extreme)/(B_SIGN+1)
        rows.append(dict(split=split,model_a=a,model_b=b,metric=metric,n_paired=n,mean_diff_a_minus_b=point,ci_low=np.quantile(bd,.025),ci_high=np.quantile(bd,.975),sign_flip_p_raw=p,bootstrap_replicates=B_BOOT,sign_flip_draws=B_SIGN,seed=SEED))
res=pd.DataFrame(rows)
# Holm correction across all 18 tests.
p=res.sign_flip_p_raw.to_numpy(); order=np.argsort(p); adj=np.empty_like(p); running=0.; m=len(p)
for rank,i in enumerate(order):
    running=max(running,(m-rank)*p[i]); adj[i]=min(1.,running)
res['sign_flip_p_holm']=adj
res.to_csv(ROOT/'paired_significance_tests_regenerated.csv',index=False)
meta={'bootstrap_unit':'line identifier; independent nonparametric resampling with replacement within each model--split','bootstrap_replicates':B_BOOT,'confidence_level':0.95,'ci_method':'percentile','paired_design':'matched line identifiers; paired bootstrap difference and two-sided random sign-flip test','sign_flip_draws':B_SIGN,'alternative':'two-sided','multiple_testing':'Holm adjustment across all 18 pre-specified paired tests','seed':SEED,'model_reruns':'No repeated API runs; line-level intervals condition on the recorded outputs and exclude provider temporal variability.'}
(ROOT/'statistical_protocol.json').write_text(json.dumps(meta,indent=2)+'\n')
print(ci.shape,res.shape)
