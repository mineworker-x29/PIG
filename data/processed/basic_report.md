# PIG 기본 OC-DFG 리포트

- Event log: `/workspace/PIG/data/raw/plasma_etcher_event_log.csv`
- OCEL: `/workspace/PIG/data/raw/plasma_etcher_event_log.ocel.json`
- Event log rows: 60
- OCEL objects: 16
- OCEL events: 60

## Object Type 분포
- aligner: 1
- foup: 1
- loadlock: 2
- loadport: 3
- lot: 1
- process_module: 4
- stocker: 1
- transfer_module: 1
- wafer: 2

## OC-DFG (상위 엣지)
### aligner
- Alignment End -> EFEM Transfer to Loadlock Start (count=2)
- EFEM Transfer to Aligner End -> Alignment Start (count=2)
- Alignment Start -> EFEM Transfer to Aligner Start (count=1)
- Alignment Start -> EFEM Transfer to Loadlock End (count=1)
- EFEM Transfer to Aligner Start -> Alignment End (count=1)
- EFEM Transfer to Aligner Start -> EFEM Transfer to Aligner End (count=1)
- EFEM Transfer to Loadlock End -> Alignment End (count=1)
- EFEM Transfer to Loadlock Start -> EFEM Transfer to Aligner End (count=1)
- EFEM Transfer to Loadlock Start -> EFEM Transfer to Loadlock End (count=1)

### foup
- Alignment End -> EFEM Transfer to Loadlock Start (count=2)
- EFEM Transfer to Aligner End -> Alignment Start (count=2)
- EFEM Transfer to FOUP End -> FOUP Unloading Start (count=2)
- EFEM Transfer to Loadlock End -> Loadlock Door Operation Start (count=2)
- FOUP Loading End -> EFEM Transfer to Aligner Start (count=2)
- Loadlock Door Operation End -> EFEM Transfer to FOUP Start (count=2)
- Loadlock Door Operation Start -> Loadlock Door Operation End (count=2)
- Loadlock Slit Operation End -> PM Slit Inbound Operation Start (count=2)
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=2)
- PM Slit Outbound Operation End -> Loadlock Slit Operation Start (count=2)

### loadlock
- Loadlock Door Operation Start -> Loadlock Door Operation End (count=4)
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=4)
- EFEM Transfer to FOUP Start -> EFEM Transfer to FOUP End (count=2)
- EFEM Transfer to Loadlock End -> Loadlock Door Operation Start (count=2)
- EFEM Transfer to Loadlock Start -> EFEM Transfer to Loadlock End (count=2)
- Loadlock Door Operation End -> EFEM Transfer to FOUP Start (count=2)
- Loadlock Door Operation End -> Loadlock Pumping Start (count=2)
- Loadlock Pumping End -> Loadlock Slit Operation Start (count=2)
- Loadlock Pumping Start -> Loadlock Pumping End (count=2)
- Loadlock Slit Operation End -> Loadlock Slit Operation Start (count=2)

### loadport
- Alignment End -> EFEM Transfer to Loadlock Start (count=2)
- EFEM Transfer to Aligner End -> Alignment Start (count=2)
- EFEM Transfer to FOUP End -> FOUP Unloading Start (count=2)
- EFEM Transfer to Loadlock End -> Loadlock Door Operation Start (count=2)
- FOUP Loading End -> EFEM Transfer to Aligner Start (count=2)
- Loadlock Door Operation End -> EFEM Transfer to FOUP Start (count=2)
- Loadlock Door Operation Start -> Loadlock Door Operation End (count=2)
- Loadlock Slit Operation End -> PM Slit Inbound Operation Start (count=2)
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=2)
- PM Slit Outbound Operation End -> Loadlock Slit Operation Start (count=2)

### lot
- Alignment End -> EFEM Transfer to Loadlock Start (count=2)
- EFEM Transfer to Aligner End -> Alignment Start (count=2)
- EFEM Transfer to FOUP End -> FOUP Unloading Start (count=2)
- EFEM Transfer to Loadlock End -> Loadlock Door Operation Start (count=2)
- FOUP Loading End -> EFEM Transfer to Aligner Start (count=2)
- Loadlock Door Operation End -> EFEM Transfer to FOUP Start (count=2)
- Loadlock Door Operation Start -> Loadlock Door Operation End (count=2)
- Loadlock Slit Operation End -> PM Slit Inbound Operation Start (count=2)
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=2)
- PM Slit Outbound Operation End -> Loadlock Slit Operation Start (count=2)

### process_module
- PM Processing End -> PM Slit Outbound Operation Start (count=2)
- PM Processing Start -> PM Processing End (count=2)
- PM Slit Inbound Operation End -> PM Processing Start (count=2)
- PM Slit Inbound Operation Start -> PM Slit Inbound Operation End (count=2)
- PM Slit Outbound Operation Start -> PM Slit Outbound Operation End (count=2)

### stocker
- FOUP Loading Start -> FOUP Loading End (count=2)
- FOUP Loading End -> FOUP Loading Start (count=1)

### transfer_module
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=4)
- Loadlock Slit Operation End -> PM Slit Inbound Operation Start (count=2)
- PM Slit Inbound Operation Start -> PM Slit Inbound Operation End (count=2)
- PM Slit Outbound Operation End -> Loadlock Slit Operation Start (count=2)
- PM Slit Outbound Operation Start -> PM Slit Outbound Operation End (count=2)
- Loadlock Slit Operation End -> PM Slit Outbound Operation Start (count=1)
- PM Slit Inbound Operation End -> Loadlock Slit Operation Start (count=1)
- PM Slit Inbound Operation End -> PM Slit Outbound Operation Start (count=1)

### wafer
- Loadlock Door Operation Start -> Loadlock Door Operation End (count=4)
- Loadlock Slit Operation Start -> Loadlock Slit Operation End (count=4)
- Alignment End -> EFEM Transfer to Loadlock Start (count=2)
- Alignment Start -> Alignment End (count=2)
- EFEM Transfer to Aligner End -> Alignment Start (count=2)
- EFEM Transfer to Aligner Start -> EFEM Transfer to Aligner End (count=2)
- EFEM Transfer to FOUP End -> FOUP Unloading Start (count=2)
- EFEM Transfer to FOUP Start -> EFEM Transfer to FOUP End (count=2)
- EFEM Transfer to Loadlock End -> Loadlock Door Operation Start (count=2)
- EFEM Transfer to Loadlock Start -> EFEM Transfer to Loadlock End (count=2)
