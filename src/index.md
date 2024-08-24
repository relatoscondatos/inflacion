---
toc: false
sql:
  ipc_items: data/ipc.parquet
  ipc_general: data/ipc_empalmado.csv
  ipc_divisiones: data/ipc_empalmado_divisiones.csv
  ipc_analiticos: data/ipc_empalmado_analíticos.csv

---

```js
import { csv, autoType } from 'npm:d3';
import moment from 'npm:moment';
```

```sql id=items_division
SELECT DISTINCT Glosa as item, Division as division
FROM ipc_items
WHERE Ano = 2024
```

```sql id=items 
SELECT DISTINCT Glosa as item
FROM ipc_items
ORDER BY Glosa
```

```sql id=divisiones
SELECT DISTINCT Glosa as division
FROM ipc_divisiones
ORDER BY Glosa
```

```sql id=analiticos
SELECT DISTINCT Glosa as analitico
FROM ipc_analiticos
ORDER BY Glosa
```

```sql id=ipc_general 
SELECT Año as año, Mes as mes, Índice as indice
FROM ipc_general
```

```sql id=ipc_division 
SELECT Año as año, Mes as mes, Glosa as item, Índice as indice
FROM ipc_divisiones
WHERE Glosa = ${selectedDivision}
ORDER BY Año, Mes, División,Glosa
```

```sql id=ipc_item 
SELECT Ano as año, Mes as mes, Indice as indice
FROM ipc_items
WHERE Glosa = ${selectedItem}
```


```js
const opcionesFechaReferencia = [
  {label: "2009", value:"2009-12-01"},
  {label: "2013", value:"2013-12-01"},
  {label: "2018", value:"2018-12-01"},
  {label: "2019", value:"2019-12-01"},
  {label: "2023", value:"2023-12-01"},
]
const fechaReferencia = view(Inputs.radio(opcionesFechaReferencia,{label: "Año de referencia (Diciembre)", value: opcionesFechaReferencia[3], format:d => d.label}));
```


# Inflación (Índice de precios al consumidor) en Chile
## 


## Índice de precios por item

```js
const optionsDivision = _.chain([...items_division]).map(d => d.division).uniq().sort().value()
const selectedDivisionItem = view(Inputs.select(optionsDivision, {value: optionsDivision[0], label: "División"}));
```

```js
const optionsItem = _.chain([...items_division]).filter(d => d.division == selectedDivisionItem).map(d => d.item).uniq().sort().value()
const selectedItem = view(Inputs.select(optionsItem, {value: optionsItem[0], label: "Item"}));
```

**Índice de precios ${selectedItem} vs Índice general**  
*Fecha de referencia (${moment(dataNormalizada_item.referenceDate).format(`MMM YYYY`)}) = 100*


```js
const dataNormalizada_item = normalizeData({dataset1: data_ipc_general, dataset2:data_ipc_item, date:fechaReferencia.value})
display(plotData({dataPlot :dataNormalizada_item.data, refdate:dataNormalizada_item.referenceDate}));
```

## Índice de precios por división (agrupación de items)

```js
const selectedDivision = view(Inputs.select([...divisiones].map(d => d.division), {value: [...divisiones][0].division, label: "División"}));
```

**Índice de precios ${selectedDivision} vs Índice general**  
*Fecha de referencia (${moment(dataNormalizada_division.referenceDate).format(`MMM YYYY`)}) = 100*

```js
const dataNormalizada_division = normalizeData({dataset1: data_ipc_general, dataset2:data_ipc_division, date:fechaReferencia.value})
display(plotData({dataPlot :dataNormalizada_division.data, refdate:dataNormalizada_division.referenceDate}));
```


```js
const data_ipc_general = _.chain([...ipc_general])
.map(d => ({
  date: moment(`${d.año}-${d.mes}`,`YYYY-M`).toDate(),
  año:d.año,
  mes:d.mes,
  indice: d.indice,
  item: "IPC General"
}))
.sortBy(d => d.date)
.value();

const data_ipc_item = _.chain([...ipc_item])
.map(d => ({
  date: moment(`${d.año}-${d.mes}`,`YYYY-M`).toDate(),
  año:d.año,
  mes:d.mes,
  indice: d.indice,
  item: selectedItem
}))
.sortBy(d => d.date)
.value();

const data_ipc_division = _.chain([...ipc_division])
.map(d => ({
  date: moment(`${d.año}-${d.mes}`,`YYYY-M`).toDate(),
  año:d.año,
  mes:d.mes,
  indice: d.indice,
  item: d.item
}))
.sortBy(d => d.date)
.value();

```


```js
function plotData({dataPlot = [], refdate= null} = {}) {
    return Plot.plot({
    marginRight:200,
    x:{grid:true},
    y:{grid:true},
    marks: [
      Plot.ruleX([refdate]),
      Plot.ruleY([100]),
      Plot.lineY(dataPlot, {
        x: "date",
        y: "indiceNormalizado",
        stroke:"item"
      }),
      Plot.text(dataPlot, Plot.selectLast({
        x: "date",
        y: "indiceNormalizado",
        z: "item",
        text:"item",
        textAnchor:"start",
        dx:5
      }))
    ]
  })
}
```

```js

function normalizeData({
  dataset1 = [],
  dataset2 = [],
  label1= "",
  label2="",
  date = null,
} = []) {

  const minDate1 = _.chain([...dataset1]).minBy(d => d.date).value()["date"];
  const minDate2 = _.chain([...dataset2]).minBy(d => d.date).value()["date"];
  const givenDate = new Date(date || minDate1)
  const minDate = _.max([minDate1, minDate2])
  const referenceDate = _.max([minDate1, minDate2, givenDate]);

  const referenceIndex1 = _.chain(dataset1).filter(d => d.date >= referenceDate).minBy(d => d.date).value()["indice"]
  const referenceIndex2 = _.chain(dataset2).filter(d => d.date >= referenceDate).minBy(d => d.date).value()["indice"]
  
  
  const dataNormalizada =  _.concat(
  _.chain(dataset1)
  .map( d => {
    const record = _.clone(d);
    record.indiceNormalizado = 100 * d.indice / referenceIndex1
    return record
  })
  .value(),
  _.chain(dataset2)
  .map( d => {
    const record = _.clone(d);
    record.indiceNormalizado = 100 * d.indice / referenceIndex2
    return record
  })
  .value()
  ).filter(d => d.date >= minDate)

  return {
    data: dataNormalizada,
    referenceDate: _.chain(dataNormalizada).filter(d => d.date >= referenceDate).minBy(d => d.date).value()["date"]
  }
}


```
