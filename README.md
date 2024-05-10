# Minecraft Mod Manager (MMM)

## Usage

1. Download the latest release from here: [Latest Release](https://github.com/joshika39/minecraft-mods/releases/latest)
2. Allow the program to download, it isn't malicious!
3. Start the program and wait for the mods to download
4. When the menu showed up, navigate to the preferred modpack and hit enter to download

#### Other useful options

- command to get the ip from the terminal: `cd $HOME\Fork\minecraft-mods\; .\print-ip.ps1`
- command to open the ports for minecraft server(25565):
  - start an **Admin** Terminal end run the following command: `cd $HOME\Fork\minecraft-mods\; .\open-ports.ps1`

## Contributing

### Setting up the project

- Fork the repository: [How to fork a repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- Clone the repository: `git clone https://github.com/<username>/minecraft-mods.git`
- Create a new branch: `git checkout -b <branch_name>` (or use a tool like [Fork](https://git-fork.com/))
- Create a Virtual Environment: `python -m venv venv`
- Activate the Virtual Environment *(if not using an IDE)*:
  - Windows: `.\venv\Scripts\Activate`
  - Linux: `source venv/bin/activate`
- Install the dependencies: `pip install -r requirements.txt`

### Making changes

- Make the changes in the code
- Commit the changes: `git commit -m "Message"` (or use a tool like [Fork](https://git-fork.com/))
- Push the changes: `git push origin <branch_name>` (or use a tool like [Fork](https://git-fork.com/))
- Create a Pull Request: [How to create a Pull Request](https://docs.github.com/en/get-started/quickstart/create-a-pull-request)

## Useful Links

#### To Search for mods

- [link search](https://www.curseforge.com/minecraft/mc-mods/mod_name/files/all?filter-game-version=2020709689%3A8203)
- [general search](https://www.curseforge.com/minecraft/mc-mods/search?category=&search=mode_name)
