### What the Script do ###
The script will read through the list of workshop links, download them, extract, and put it all in one folder.
The maps will be downloaded from "http://steamworkshop.download/".

The code isn't good, it's pretty messy. 
Multi Threading is used to speed up the process of downloading.
Look through the code and make changes if you like.


### Tutorial ###
Install Python 3
Run the script to install required package and make a text file for you to put the workshop links.
Open the file "Workshop Download List.txt".
Enter workshop link in new lines, look in "Workshop Link List.txt" for example.

Optional: Copy the list of workshop links inside "Workshop Link List.txt". (Top 150, Most Popular, All Time)
https://steamcommunity.com/workshop/browse/?appid=824270&browsesort=trend&section=readytouseitems&actualsort=trend&p=1&days=-1

Run the script again and it should be downloaded and extracted to the parent folder. (The Folder Before This One)
Copy all the map files (.sce files) to the kovaaks map folder.
Path_To_KovaaK's\FPSAimTrainer\Saved\SaveGames\Scenarios
Skip or Replace any existing ones, and you're done.
