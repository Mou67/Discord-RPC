# Discord RPC-Python

This project is a Python script that integrates with Discord's Rich Presence feature, allowing you to display custom status messages on your Discord profile.

## How to use

1. Create a new Application in [Discord Appliction](https://discord.com/developers/applications) and set it up like you wish.
2. Copy the Application ID from your Application and paste it into the config.json file.
3. Customize the Presence as you want.
4. Now run the script **Start.py**.

## System Information Keys

The following keys are used to replace placeholders in the configuration:

- %cpu%: CPU usage percentage
- %cores%: Number of CPU cores
- %ram%: RAM usage percentage
- %ram_total%: Total RAM in GB
- %ram_used%: Used RAM in GB
- %ram_free%: Free RAM in GB
- %disk%: Disk usage percentage
- %disk_total%: Total disk space in GB
- %disk_used%: Used disk space in GB
- %disk_free%: Free disk space in GB
- %time%: Current time (HH:MM:SS)
- %date%: Current date (YYYY-MM-DD)
- %uptime%: System uptime (HH:MM:SS)
- %hour%: Current hour
- %minute%: Current minute
- %second%: Current second
- %day%: Current day
- %month%: Current month
- %year%: Current year
- %weekday%: Current weekday
- %os%: Operating system
- %hostname%: Hostname of the machine
- %username%: Username of the logged-in user
- %ip%: IP address of the machine

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Made by Mou67