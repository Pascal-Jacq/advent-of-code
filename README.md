# advent-of-code
My setup to quickly hack my way through the daily advent of code problem

# Install 
If you want to use codespace : Just click "code" button and go!

If you are using Visual Studio Code : Install the dev container extension, then run "Rebuild and Reopen in container"

If you are using python : pip install -r requirements.txt

# Usage
To generate and open a notebook ready to today's puzzle

From inside the dev container just type : "go" or : "go {day} {year}" 

From a terminal type : "python advent.py" or "python advent.py {day} {year}"
Then open the generated notebook using your jupyter notebook/lab/hub

# Configuration
You have to retrien your session cookie and create a session.json file with the cookie

When logged on https://adventofcode.com/:
- Right click on the page then click "inspect" :![pic1](https://user-images.githubusercontent.com/9217388/207906844-f63cef66-b1c9-4319-82ea-137a022379bb.png)
- Click Application, then Cookies, then locate "session" and copy the associated value ![pic2](https://user-images.githubusercontent.com/9217388/207907531-1f554fb7-9aa8-446c-8880-8fbef3c1538b.png)

- You can now paste this value in your session.json file
