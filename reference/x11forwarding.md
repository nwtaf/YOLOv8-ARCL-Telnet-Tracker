# x11 Forwarding
Not sure if any of this is required after Bookworm replaced X11 with wayland/wayfire...
## Raspberry Pi Configuration
### Enable SSH:
- GUI: Preferences>Interfaces>Enable SSH
- Terminal: `sudo raspi-config`>Interfaces>Enable SSH
### Install X11 Server:
- `sudo apt-get install xserver-xorg`
### Configure SSH for X11 Forwarding:
- Open the SSH daemon config file with: `sudo nano /etc/ssh/sshd_config`
- Make sure the following lines are present and not commented out: 
`X11Forwarding yes`
`X11DisplayOffset 10`
     - Note: X11Forwarding was enabled by default, X11DisplayOffset 10 was not, and is not necessary to enable, but it is a best practice to enable.
- Save and close the file, then restart the SSH service with: `sudo service ssh restart`

## Windows Configuration
### Install X11 Server:
- Xming or VcXsrv (branch of Xming). Both are free. Make sure X11 server is running when trying to connect via SSH to pi.

### Install SSH Client that supports X11 forwarding:
- PuTTY Configuration>Connection>SSH>X11>Enable X11 Forwarding
