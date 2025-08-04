# Hi!

This is meant to help people make AP worlds even if they have 0 experience programming. I tried my best to give a ton of explanation but I know its not perfect.
All of the explanations are kinda just me yapping so they could be unhelpful or super helpful, it all depends on the background of the person reading! I included a lot of explanations on basically every step including getting your fork and what the hell a github is.

The most important thing though is that you take this slow. Youre doing an AWESOME job just by reading this to see if it helps you. And if it doesnt, thats fine!
Theres no pressure to get anything out in any time period.

The other most important thing is that this is only one of the resources you have available to you. Theres tons of AWESOME people in the archipelago discord that are primed to answer any question you have. There's no bad questions! Whether it's the first time you've opened code, or if you've been programming for years, don't be afraid to ask for help. I know how hard it can feel to ask for help but trust me, people are more excited to help then anything else.
If you are worried about messaging in a large group chat then message me directly! My name is Nep (I have the profile pic of a cute rat). Im also super shy and awkward so Id love love love to help others that also feel that way.

# How do you make use of this?

Well theres a bunch of ways! To start though, you gotta first make a github account and fork the [Archipelago](https://github.com/ArchipelagoMW/Archipelago) project. Its above the big green Code button, sandwiched between the Watch and Star buttons.
![Image](https://github.com/user-attachments/assets/4a56598b-d467-4a5a-9743-efbb1ca45a41)

Name the repository whatever you want and make sure you make yourself the owner (Github is also really weird and you can only fork a project once on your account. There are work arounds though if you need). Now you want to open up your command terminal and navigate to where you want to place your project. Ill leave some helpful ways of using terminal at the bottom of this. Clone your repository (it will go into its own folder based on the name of the repository) and open it up in whatever you use to program! I recommend [Visual Studio Code](https://code.visualstudio.com/). If you hate AI like me, then dont worry you have to enable it in an extension.

Now that you have your cloned Archipelago project, go to the worlds folder and create a new folder for your game. Now you can manually create all the files and write everything yourself or just copy these files and drop them in. If the file names are green that means they were newly added. Once you have the files in, I would push them up and make sure that its working and that you are able to commit everything. Again, Ill add some more specific details about what that means and how to do it at the bottom if you need it.

After that, youre good! You can start replacing all my unfunny comments with actually important stuff. Dont worry about "good" code or what it looks like. If it works, then its 10/10 no notes. Also dont be scared of errors! Run the generation as many times as you want. Errors are great cause they tell you what you need to fix or what to do next. They are great at guiding you. If you need help reading errors, then theres tons of people that can help you!

# Command Line/Terminal/Whatever

If you have multiple drives like a C and D drive then you can go to that drive just by putting the name of the drive followed by a colon into the terminal. It really is just that simple. When you want to move around then you use `cd`. As an example, if I wanted to go to my D drive and then go to a folder I created called workspace it would look this this.

`>D:`

`>cd workspace`

~~If you capitalized workspace then it needs to be capitalized when you cd into it as well~~ Thats not true lol! Just type in the name you want. You can also use the TAB key to autocomplete file names. So instead of typing the entire word workspace you could just type `wor` and then hit tab and it will fix it for you. If you had more folder or file names that have that same `wor` starting condition then just keep hitting tab until you find it. Another important thing to mention is if you want to go backwards a folder. To do that you do `cd` followed by 2 periods.

`>cd ..`

A lot of people have workspace folders. Its nice to just hold all youre projects in one location. And Im sure youll definitely fall in love with programming from this and go on to become the best dev ever right?

# Git commands

Below Ill list a bunch of git commands and Ill have a description of what its doing next to it. I am not a prolific github user so this is nowhere near all of them. If you have other questions about what they do or why its not working, then again, asking is a great option.

`git clone the-name-of-your-repository` - This is how youll download your repository. Downloading it this way doubles up as letting you then perform the git push that are explained later. You can get the text you put after the word clone by clicking the green Code button thats on YOUR repository and then copying the text under HTTPS. There are other options but I wont go into them here but feel free to explore and learn!

![image](https://github.com/user-attachments/assets/5884471a-dcf9-4d1e-9ffb-a596ce767fa7)

`git status` - This guy tells you what branch youre on, what files have been changed, and what files are ready for committing. I spam this one all the time tbh. Honestly sometimes Ill just type it twice in a row and honestly I dont know why.

`git pull` - This gets all the changes that were made to the branch (explained below) and puts them on your computer. Important for if you are working with others!

`git add file-name` - This readies a changed file to be committed (explained below). If the file name is red when you type git status then its not readied and if its green then it is

`git commit -m "Some text about what you did"` - This is the committing. Basically you bundle up all the changes and get them ready to send to github all at once. Its generally good to add some descriptive text but I get it....sometimes you just keyboard smash and thats ok. Its also generally nice to do regular commits. For example, committing after you finish the Items file or fix up a specific bug

`git push` - This takes your commits and sends them to github. If its your first time pushing up that specific branch then itll error out and tell you to do a set-upstream thingy. Just copy whatever if tells you to and use that.

`git checkout name-of-branch` - Switches to the branch that you name. If you created a branch on github or someone youre working with did then youll need to do a git pull first.

`git checkout -b name-of-new-branch` - This creates a new branch on your computer locally. Nice to quickly swap to a new branch without needing to create it on github, do a pull, then switch to it. If you do this and then do your git push youll get that set-upstream thingy.

`git branch` - Lists all the branches you have locally on your computer. Nice if you want to switch to a branch and youve forgotten the name/dont wanna type it and just wanna copy it.

`git merge name-of-other-branch` - This ones more complicated (its why I gave it extra space). Its main use is for bringing in changes from another branch into yours. For example, lets say you branched off your main branch and called it my-first-branch. After working on a few things you decide to leave it alone for a while and work on something else. You branch off of main again and this time call it my-second-branch. You are able to finish up your second branch and you successfully merge (merging will be extra explained just below so dont worry if you dont get it yet) it into main. When you go back to working on my-first-branch then youll want to run git merge main so that all those changes that you finished in your second branch get moved over to this branch as well.

As discussed this is just the functional basics. You could make an apworld and get it up on github with just these commands and maybe not even all of them. However theres sooooooooo much more to learn with git. phaneros in the AP discord has a wonderful [intro to git]((https://github.com/MatthewMarinets/ap_sc2_notes/blob/main/git.md)) that gets more in the weeds. Also if you're somehow here without going through the discord (???) then you can find the thread [here](https://discord.com/channels/731205301247803413/1400827971123675247) to ask for help.

# Other GitHub stuff

## What the heck is a branch?

A branch is like the fork you made for your archipelago changes but at a smaller scale. Its super duper useful for making sure you dont mess anything up. Youll start with your main branch by default. Then you can branch off of that to start adding features or fix bugs.

## Why would I use a branch? Can't I just push it up to main?

The first reason to use them is if you are working with other people. It helps divide the work and make sure you dont overwrite others work. If we were both working on something at the same time and you push up some code and afterwards I also push up my changes but I dont do a git pull first, then all your changes would get overwritten. Branches help protect from that.

If youre working alone then branches are still super useful! They help you organize any different features and bugs youre working on so you could work at multiple at once without confusing yourself. Its also super helpful for if stuff starts to mess up. For example, if you had a working AP world and you pushed up some code that broke a lot of stuff that you didnt realize, if you pushed it up to main then it gets really complicated to fix it. If its on its own branch then in the worst case scenario your main branch is still protected since you havent merged those changes yet. It could also be useful to create a backup branch that you occasionally merge main into so that if your main does get really funky, you can avoid the absolute worst case.

## Ok Im using branches but what the heck is merging?

Merging is just combining the branches into one. The simplest way is after you do your final git push, if you go to the github website on your repo and refresh, you should see a new button that says compare & merge. Go ahead and click that and youll see how youre new branch compares to the one youre merging into. If youre good with those changes then click merge. If youre working with someone else, then you can use this to show them what changes youre making and they can double check your work. There can be a bunch of complications with merging (if you keep programming you will eventually encounter the horrors that some merge conflicts can bring) so if you are still struggling with understanding feel free to reach out!

# Troubleshooting

## This takes forever to test. How do you do it faster?

The fastest way I like to do this is use the fun little terminal button at the bottom of visual studio. If you dont see it, put your mouse right above the blue bar down there and you should see your mouse turn into the vertical stick with arrows on either end. Click and drag upwards to reveal a brand new section. From there you can go to the terminal tab. It should already be located in the correct folder but if it isnt use the command line navigation that was described earlier to get to the upper most folder. That'll be whatever you named your fork when you first made it. From there you can do a couple of things that help speed up development. You can use `py .\Launcher.py` to get an instance of the archipelago launcher up. This is the best way to quickly generate template options to make sure the yaml is generating correctly. `py .\Generate.py` does your generation because clicking the button in that launcher doesnt actually work. It just sends you to the Generate.py file. 

Finally, you can do `py .\WebHost.py` to spin up your own local instance of the archipelago website. It may ask you to install a few things like flask or pip so if you dont want to then feel free to skip this step. You may also encounter a bunch of errors that are hard to trace back. I wont go into explicit detail here on how to debug it but if you are able to get it running, to access the site simply type `localhost` in your browser.

## Uhhhhh.....wheres my yaml file?????

If you went and used the launcher to make your yaml file for testing and it simply is not there, then thats youre queue to go error hunting. The best way to start is to scroll through the terminal log and see if you can find your file name. You should see a pretty accurate description of what went wrong. Most of the time it should be an easy fix like a typo here or there. Sometimes it can be more complex and lead to other issues down the line. The important part is to take the debugging process one step at a time. Dont feel bad about seeing errors, but embrace them as your best mentor. Once you clear the error, a second new error may pop up in its place. New errors are exciting! That means you made progress!

## Debugging is scary and makes no sense. Theres so many colors and lines and symbols all over the place how do I read this?

Excellent question! Im not gonna lie, theres a lot of irrelevant information in error messages sometimes so learning how to figure out whats important and whats not is a skill that takes time to learn. The main things you'll want to look for is anything that has your file name in it. Here's an example from when I was debugging this test world so that it would generate yamls and actual make a world. Ignore the fact that it is talking about Sly1 I just borrowed that archipelago install for testing.

![Image](https://github.com/user-attachments/assets/2ac37a63-9d72-45fe-bec5-0bbe2f596071)

Now this is confusing and has a lot of scary purple but what does it actually mean. The first thing I do is I look at those files. The first 6 are all errors that are in files that are in the base `worlds` folder of archipelago. Now I know that I didnt touch any of those files so they shouldnt be the ones that are broken. The 7th though reveals the real issue. In my `__init__.py` I tried to get the name of the starting chapter like this `starting_chapter = chapter_type_to_name(ChapterType(self.options.StartingChapter))`. The issue is that thats not how enums work. I actually needed to use square brackets `starting_chapter = chapter_type_to_name[ChapterType(self.options.StartingChapter)]`. Its a super tiny difference but one works and one crashes. 

In a couple of different spots in the init.py and Items.py youll see some commented out print statements. Those are also left over from my own debugging process. I like to spam print statements all throughout my code where things are breaking so I can see exactly how far things are going and what certain variables may look like. Its really nice to add large swaths of hyphens or a bunch of emojis so that its easy to see when your scrolling through the logs (logs being what comes out when you run the terminal code). Abuse them. Spam them as much as you want no one can stop you.

## Ok so I found my error but I have no clue how to fix it

Google it! No seriously copy the error and paste it into google (i swear to god if you use chatGPT id get it but id be a little peeved). Theres a million difference sites that have decades of forum posts that will have your issue 9 times out of 10. Stack overflow is the one that everyone memes about but its real. The entire tech industry is reliant on posts from 2016 on stack overflow with 6 upvotes. Outside of that theres always the dev channel in archipelago. Theres tons of helpful people in there that are more than happy to help and dont feel ashamed if the fix is changing out parenthesis for square brackets. Everyone goes through this and its so easy to miss things like this when your 6 hours deep in a debugging session and youre starting to get frustrated on why it just wont work. Once again if you are too worried about posting your message out in the open, dm someone! Ill mostly be available (Nep again :3) and respond where I can. If I cant directly answer your question Ill try to get you pointed in the correct direction of where to look.
