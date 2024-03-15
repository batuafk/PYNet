> [!WARNING]
> If Server.py is not opening run this cmd: ``taskkill /f /im python.exe`` or ``pkill python``

- [x] Server loads 'socket_host, socket_port, web_host, web_port' from config.env
- [x] Web server
- [x] Handles clients without ping
- [x] Client copies himself to shell:startup if OS is Windows
- [x] Send python codes by adding "#exec" to the first line in the input
- [x] Send self python codes by adding "#exec ip:port" to the first line in the input
- [ ] Clients CPU, GPU, WiFi usages on plots
- [ ] Cant run Client if its already running
