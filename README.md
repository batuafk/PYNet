# Needs update

> [!WARNING]
> If Server.py is not opening run this cmd: ``taskkill /f /im python.exe`` or ``pkill python``
>
> Send #exec codes cautiously to prevent the client from getting stuck in an infinite timeout

- [x] Server loads 'socket_host, socket_port, web_host, web_port' from config.env
- [x] Handles clients without ping
- [x] Client copies himself to shell:startup if OS is Windows
- [x] Send python codes by adding "#exec" to the first line in data input
- [x] Send self python codes by adding "#exec ip:port" to the first line in data input
- [x] If your client doesn't receive output from your #exec code, it sends b"no output"
- [ ] Clients CPU, GPU, WiFi usages on plots
- [ ] Cant run Client if its already running
- [ ] ID for each client

![image](https://github.com/Bt08s/PYNet/assets/68190921/c4e9a1e3-ec26-4090-b086-bd92055401a5)
