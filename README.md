curl http://pixta.local:5000/health.json
curl -X POST http://pixta.local:5000/change_mode.json
curl -X POST -H "Content-Type: application/json" -d '{"color": "#ff1493"}' http://pixta.local:5000/change_static_color.json

curl -X POST -H "Content-Type: application/json" -d '{"colors": "#ff5733, #e30b5c, #40e0d0"}' http://pixta.local:5000/change_cycle_colors.json
a