from pathlib import Path

index = Path(__file__).resolve().parents[1] / "app/src/main/assets/index.html"
text = index.read_text(encoding="utf-8")
text = text.replace(
    "grid-template-columns:32px 1fr 1fr 1fr 36px",
    "grid-template-columns:32px 1fr 1fr 1fr 42px 36px",
)
text = text.replace(
    "grid-template-columns:28px 1fr 1fr 1fr 34px",
    "grid-template-columns:28px 1fr 1fr 1fr 38px 34px",
)
text = text.replace(
    "s.currentWorkout=WORKOUTS[raw?.currentWorkout]?raw.currentWorkout:'A';return s}",
    "s.currentWorkout=WORKOUTS[raw?.currentWorkout]?raw.currentWorkout:'A';s.history=s.history.map((x,i)=>Object.assign({id:x.id||('h_'+i+'_'+(x.date||Date.now()))},x));s.measurements=s.measurements.map((x,i)=>Object.assign({id:x.id||('m_'+i+'_'+(x.date||Date.now()))},x));return s}",
)
index.write_text(text, encoding="utf-8")
print("Ajustes finais da interface v5 aplicados")
