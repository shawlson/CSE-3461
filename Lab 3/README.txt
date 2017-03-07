Dan Shawlson
CSE 3461, T/Th 12:45
Lab 3

Start the FTP server on gamma.cse.ohio-state.edu with the command:
    python3 ftps.py <port number>
Note that the server will receive only one file before it exits.

Start the troll process on beta.cse.ohio-state.edu with the command:
    troll -C <IP-address-of-beta> -S <IP-address-of-gamma> -a <client-port-on-beta> -b <server-port-on-gamma> -r -s 1 -t -x 0 <troll-port-on-beta>
Use 127.0.0.1 for <IP-address-of-beta>. The <client-port-on-beta> is hardcoded to be 5195.

Initiate a transfer with the FTP client on beta.cse.ohio-state.edu with the command:
    python3 ftpc.py <IP-address-of-gamma> <remote-port-on-gamma> <troll–port-on-beta> <local-file-to-transfer>