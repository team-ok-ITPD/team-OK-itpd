# Customer meeting transcript

- **Date:** 2026-10-26
- **Participants:** adelazzi, Customer

[00:00:03] adelazzi: We're gonna start now.

[00:00:04] adelazzi: Uh, can you— could you tell me please, you can see my screen or not?

[00:00:14] Customer: I can see it now.

[00:00:16] adelazzi: Okay, this is our page.

[00:00:23] adelazzi: Let me— This is the login screen.

[00:00:27] adelazzi: This is the creating user screen.

[00:00:29] adelazzi: I already have account, so we start with login.

[00:00:34] adelazzi: For now it's clickable, as I showed you before the prototype, Figma prototype.

[00:00:43] adelazzi: Now it's clickable.

[00:00:47] adelazzi: Uh, let's go take an example.

[00:00:51] adelazzi: Or you want me like show you the details of the screen?

[00:00:54] adelazzi: What's that mean?

[00:00:55] adelazzi: What does this mean?

[00:00:59] Customer: Uh, yeah, I'd like to look at this screen first.

[00:01:05] adelazzi: Okay, this screen is the form screen.

[00:01:10] adelazzi: Uh, before it was the language was here in the top and you mentioned it's not good because it's one of the important things, so I take it down.

[00:01:21] adelazzi: Here we're going to choose the language, the difficulty, and here the topics.

[00:01:26] adelazzi: For now, those are the bugs which is stored before in our backend from the other users.

[00:01:38] adelazzi: Here the AI generator, so we're going to ask AI and so on.

[00:01:44] adelazzi: It's not available for now.

[00:01:46] adelazzi: I need the API key, but here the prepared one which is already in the backend and the database.

[00:01:54] adelazzi: Okay, let's take one as example for this one.

[00:01:56] adelazzi: This is the description of this bag.

[00:02:02] adelazzi: Okay.

[00:02:03] adelazzi: Okay, here we're gonna start, start participant.

[00:02:07] adelazzi: It goes to the screen.

[00:02:11] Customer: Okay.

[00:02:12] adelazzi: The screen have the code.

[00:02:16] adelazzi: You can edit on it.

[00:02:19] adelazzi: We're going to test that.

[00:02:20] adelazzi: This is the debug console.

[00:02:22] adelazzi: So if we run it, we will see the debug console here.

[00:02:27] adelazzi: This is the test, the 3 tests.

[00:02:31] adelazzi: We can run each one of them if you want to.

[00:02:34] adelazzi: As you see here, The debug console is changed.

[00:02:40] adelazzi: We're going to run each one or run all of them with this button.

[00:02:45] adelazzi: We can edit on it like that, the input and output.

[00:02:52] Customer: You can edit the output?

[00:02:54] adelazzi: Yeah, editing the test, like add the new test we like.

[00:02:59] adelazzi: Like for this example, we have Uh, the calculated total sum score.

[00:03:08] adelazzi: Uh, we can edit here.

[00:03:10] adelazzi: Let's take an example: 1, 2, 3.

[00:03:15] adelazzi: We know the, the sum of those are 6.

[00:03:21] adelazzi: Yeah.

[00:03:23] Customer: Okay.

[00:03:24] adelazzi: We save it.

[00:03:26] adelazzi: So we have the new test.

[00:03:29] Customer: So who created these tests, all the 3 tests?

[00:03:34] adelazzi: For initial test, it's created by us, by the AI.

[00:03:41] adelazzi: But here we give the permission to the user to add his tests as he wants.

[00:03:48] adelazzi: This is new for him.

[00:03:51] Customer: It's not a new test, it's-

[00:03:54] adelazzi: Editable.

[00:03:55] Customer: Okay, it is a new test, yeah, but why do you let the user edit the original tests?

[00:04:03] Customer: The original tests were like source of truth.

[00:04:08] Customer: They were like created by the author, by the AI, and they were guaranteed to be like correct.

[00:04:17] Customer: Like they failed when the program was buggy, they passed when the program was Correct.

[00:04:24] adelazzi: Actually, I get this idea from LeetCode because LeetCode gives us like access to editing these tests.

[00:04:34] adelazzi: There is another test.

[00:04:35] adelazzi: Those 3 are only for seeing the— giving the user accessible.

[00:04:41] adelazzi: And there is another test.

[00:04:42] adelazzi: It's not like—

[00:04:43] Customer: I think, I mean, default tests should not be editable.

[00:04:48] adelazzi: Okay.

[00:04:49] adelazzi: I-

[00:04:50] Customer: mean, yeah, like new tests, yeah, can be editable.

[00:04:55] Customer: But those are like the source of truth.

[00:04:58] Customer: So why edit them?

[00:05:00] adelazzi: Okay.

[00:05:01] adelazzi: Okay.

[00:05:02] adelazzi: So could you please tell me if we add a new thing here, which is like the truth test, and here let the user add and edit his own tests.

[00:05:14] Customer: Yeah, that, that would be okay.

[00:05:19] Customer: Yeah.

[00:05:20] Customer: Uh, however, uh, what am I looking at right now?

[00:05:23] Customer: Is it MUP or is it how you see your product, like the ultimate version?

[00:05:31] adelazzi: Uh, for now we can say it is, uh, MUP, but okay, and MVP, but there is new features they didn't add it yet.

[00:05:42] adelazzi: Like the other languages, uh, programming languages, like the AI itself is not integrated yet.

[00:05:51] adelazzi: Right.

[00:05:52] Customer: So I mean, we discussed, um, some, some other interface for code editing.

[00:06:00] Customer: Uh, what are your plans?

[00:06:03] Customer: Yeah, I mean, I, I told that, uh, I'd like to use VS Code as a code editor.

[00:06:10] Customer: I think we discussed that a couple of times.

[00:06:14] Customer: So how do you see integrating VS Code into your product?

[00:06:21] adelazzi: Actually, for now we've seen the VS Code, we tested, we have the VS Code itself, but there is problem here.

[00:06:29] adelazzi: When we get, when we open the code or the debug in the VS Code, we can't like test it.

[00:06:37] adelazzi: We can't like do something on it.

[00:06:41] Customer: What do you mean?

[00:06:42] adelazzi: So if we like get this code and run it maybe in somehow in VS Code online editor.

[00:06:52] Customer: Okay.

[00:06:53] adelazzi: I have my friend do that before, did that before, but we get problem there, which is like how we can submit from VS Code online editor. how we can, uh, how can I say it, how we can run those tests in this VS Code online editor?

[00:07:13] Customer: Well, you can create a VS Code extension which will communicate with the site and submit.

[00:07:23] adelazzi: That's what, that's what, uh, one of us like in the team told me before.

[00:07:28] adelazzi: We need to create an VS Code extension.

[00:07:33] adelazzi: So, so this is the solution.

[00:07:35] adelazzi: This is the only solution.

[00:07:36] adelazzi: We need to create a VS Code extension.

[00:07:41] Customer: Uh, with VS Code?

[00:07:43] Customer: Well, this is not the only solution.

[00:07:47] Customer: Uh, if you can—

[00:07:49] adelazzi: Because now I get all the functions of the VS Code, so we can, we can test that.

[00:07:53] adelazzi: Like when we run this, we have the errors, we have the debugs here.

[00:07:58] adelazzi: We can like make it, fix it like that.

[00:08:01] adelazzi: It's 0.

[00:08:02] Customer: No, there are not all functions.

[00:08:04] Customer: Like, can you go to definition for a variable?

[00:08:07] Customer: Can you debug the program?

[00:08:09] Customer: Like debug mode?

[00:08:11] Customer: Yeah, yeah, we can add it.

[00:08:14] Customer: I mean, it will be like so much effort to add these things.

[00:08:19] Customer: Uh, yeah, I told you that like in the first meeting, I guess. that you can explore this direction, but I'm not sure if you like explored it deep enough to understand how much effort it will require, like adding a language server somehow, adding like extensions for every language, adding some functionality like linting, type checking and so on.

[00:08:52] Customer: So I still think that VS Code is like the only viable option, like, and that it should somehow be a part of the product, maybe as a web version, like in browser, or a standalone application.

[00:09:12] Customer: So you asked like how like whether extension is the only way.

[00:09:20] adelazzi: Yeah.

[00:09:22] Customer: It might not be the only way.

[00:09:24] Customer: So for example, you just replace this editor with VS Code and somehow make VS Code like in the browser, somehow make VS Code talk to the other parts of your site... like this run test button or submit solution button.

[00:09:47] Customer: So basically, like, you keep the logic, most of the logic on the site and use VS Code just for code editing, debugging, and so on.

[00:10:02] Customer: So maybe, yeah, you will still need to write a little this code extension, but most of the logic may be on the site as well.

[00:10:16] Customer: I'm not sure if this can work, but this is what experiments are for.

[00:10:23] Customer: You can explore this direction.

[00:10:28] adelazzi: Okay, actually I try to imagine if we open like I have VS Code here.

[00:10:36] adelazzi: Let's open it quickly.

[00:10:39] adelazzi: Okay.

[00:10:39] adelazzi: VS Code, main editor.

[00:11:06] adelazzi: Okay, like that.

[00:11:12] Customer: Maybe it can be like an iframe with VS Code and your site can somehow talk to it.

[00:11:24] adelazzi: Okay, here if we Like directly open that in, how we can say it, the bug.

[00:11:33] adelazzi: Let's say we can see here the code of the bug and so on.

[00:11:37] adelazzi: How we can submit?

[00:11:39] adelazzi: This is what I want to imagine.

[00:11:43] adelazzi: How we're going to test the code itself?

[00:11:45] adelazzi: Let's say it like that.

[00:11:48] Customer: Yeah, I told you.

[00:11:49] adelazzi: I have now Python code.

[00:11:51] Customer: So open, like, click the file, the file button on the left.

[00:12:00] adelazzi: Yeah.

[00:12:01] Customer: Okay, see, here is a sidebar.

[00:12:05] Customer: Okay, and here are buttons: open folder, open recent.

[00:12:09] adelazzi: So yeah, so we need to create something like that, have button of submit, button of test, and so on.

[00:12:19] adelazzi: Uh, yeah.

[00:12:21] Customer: Yes, like I think this is like the most portable version, the most like the version, uh, which you can use outside of your platform, like your build, what you're building, uh, like because I cannot use a standalone VS Code not in the browser.

[00:12:45] Customer: Install your extension, then connect to your site, and then basically do everything from this extension.

[00:12:53] adelazzi: But there is another solution.

[00:12:56] adelazzi: What if we just import the SSH from here and go here, or maybe to the VS Code locally?

[00:13:04] adelazzi: I mean, the desktop app, or here also we can like add only the SSH and that's it.

[00:13:15] Customer: I mean...

[00:13:16] adelazzi: is it acceptable like that with your own extension, with your everything, without editing anything here?

[00:13:27] adelazzi: So just go here, put in the extension and so on.

[00:13:35] Customer: I mean, yes, you can have pre-installed extensions.

[00:13:39] Customer: And you can probably connect from this browser VS Code to a server with your environment and with the test files and exercise files.

[00:13:54] Customer: So this is, this is all right, like you can probably— I don't know—

[00:14:01] adelazzi: Avoiding like creating an extension in VS Code and so on for-

[00:14:05] Customer: Avoiding creation.

[00:14:07] Customer: I'm not sure you will be able to do that.

[00:14:10] Customer: Like, how do you submit a problem?

[00:14:14] Customer: Like, I mean, the solution.

[00:14:15] Customer: How do you run the test?

[00:14:20] adelazzi: Yeah, that's—

[00:14:22] Customer: Where do you read the exercise statement?

[00:14:26] Customer: Like, what do you do if the server disconnects?

[00:14:33] adelazzi: Yeah, so we need the extension, we can't avoid it, but we can do— we can run the VS Code online version or the VS Code desktop with SSH.

[00:14:47] adelazzi: This is the solution.

[00:14:50] Customer: Yes, I think this is a solution.

[00:14:52] Customer: This is the solution.

[00:14:55] Customer: Okay, and Like, you can choose how much logic should be in the extension.

[00:15:07] Customer: Maybe, maybe like go to your site.

[00:15:14] adelazzi: Okay.

[00:15:15] Customer: So you see everything like in the middle, like the code editor, the debug console.

[00:15:22] Customer: For example, every— this is replaced with VS Code.

[00:15:27] adelazzi: Okay.

[00:15:27] Customer: Everything stays, yeah, the sidebar stays on the left, the sidebar stays on the right, and just like the middle is replaced with VS Code.

[00:15:38] Customer: And then you click run tests and the tests run basically, and you see the output somewhere, maybe in VS Code. inside VS Code.

[00:15:50] Customer: So you can—

[00:15:52] adelazzi: Yeah, here, this is the output of the console.

[00:15:54] Customer: Yeah, I mean, uh, clicking Run Tests on the right will run some command inside VS Code.

[00:16:05] adelazzi: Okay.

[00:16:05] Customer: And show the output in the terminal.

[00:16:08] Customer: So your extension will be like a daemon Just for your side to like send commands to VS Code.

[00:16:21] Customer: You get the idea.

[00:16:23] adelazzi: Let me write this one, like possibility for change only the meta box with VS Code.

[00:16:32] Customer: Yeah, but like the problem is that VS Code looks better on a widescreen.

[00:16:40] Customer: Yeah, I do.

[00:16:40] Customer: And if you put it just in the middle, yeah, it's bad.

[00:16:44] Customer: You don't have enough space.

[00:16:46] adelazzi: Yeah, I think it will be good if we— I want your validation for this one.

[00:16:52] adelazzi: Why we can like let it like that and here in this place, you can see my mouse.

[00:16:59] Customer: Yeah.

[00:16:59] adelazzi: Put in a button which is like send you directly to the VS Code IDE online.

[00:17:05] Customer: Okay, what happens then?

[00:17:07] adelazzi: And this one, it will be like for maybe the light users, maybe from the phone or something like that.

[00:17:13] adelazzi: But if we click here, it will send us directly here with our code and so on and link it with SSH.

[00:17:23] Customer: Hmm.

[00:17:24] adelazzi: What did you think about that?

[00:17:25] Customer: Okay.

[00:17:27] Customer: From the first glance, sounds cool.

[00:17:32] adelazzi: And so given-

[00:17:32] Customer: Like mobile user friendly.

[00:17:35] adelazzi: Yeah, a lot of options for users.

[00:17:36] adelazzi: We don't like just take them in one place.

[00:17:39] Customer: But okay, I didn't consider any mobile users like for this project.

[00:17:46] Customer: I think it shouldn't be lighter.

[00:17:52] Customer: Like, I think it's like a normal— I think it's directed towards desktop users who use like real tools, real IDEs. real code editors, and usually I consider the target audience are like students on the labs at the university, so they, they come with their own computer, not with the phone, and they solve the exercises to learn something.

[00:18:26] adelazzi: Okay, okay.

[00:18:28] Customer: And so I see.

[00:18:31] Customer: I'm not sure if it like can really be done mobile-friendly and if we should spend time on this.

[00:18:38] adelazzi: No, no, we don't need to spend, but we can— we're gonna add it like a delighter in the documents.

[00:18:45] Customer: Yeah, uh, I mean, since it's directed towards desktop users, it's not a delighter, it's a must-have feature to be able to Open an exercise in VS Code and solve it there.

[00:18:59] adelazzi: Okay, so, okay, so I need to add VS Code.

[00:19:05] adelazzi: It's a need, VS Code.

[00:19:07] adelazzi: Other VS Code?

[00:19:08] Customer: Yeah, must have.

[00:19:10] adelazzi: Yeah, IDE, and link it with SSH.

[00:19:16] adelazzi: Creating extension.

[00:19:25] adelazzi: For this, for link with website.

[00:19:36] adelazzi: Okay, I think that's it.

[00:19:40] adelazzi: Um, what do you expect from us for the next meeting?

[00:19:47] Customer: So I expect to see good integration, okay, and the fully working scenario, like one, preferably like 2 of them.

[00:20:02] Customer: Like one of them, yeah, go log in on the site, choose an exercise, like open it in VS Code, solve it, submit.

[00:20:18] adelazzi: Okay, for now the, the features are running.

[00:20:23] adelazzi: We only need like to add it to the VS Code.

[00:20:27] adelazzi: I can show you some examples like this one.

[00:20:31] adelazzi: We have unique items, like removing the duplication from the, the code and so on here.

[00:20:40] adelazzi: This is the problem.

[00:20:42] adelazzi: So we run the test.

[00:20:44] adelazzi: He mentioned we have one failed, which is this example.

[00:20:49] adelazzi: It gives us 2, 2, 3, 2.

[00:20:51] adelazzi: We expecting 2 and 3, removing the 2 repetition, but the answer is 2, 2, 3, 2.

[00:21:00] adelazzi: Okay.

[00:21:04] adelazzi: The solution is here.

[00:21:06] adelazzi: This is the solution, is adding this to the scene.

[00:21:18] adelazzi: Because as we see here, the problem is here.

[00:21:23] adelazzi: Like, he go to the items, item after item, but he didn't like record him in the scene.

[00:21:30] Customer: Okay.

[00:21:32] adelazzi: So yeah, when we run this, all the checks are passed and that's it.

[00:21:40] adelazzi: It's right now solved.

[00:21:43] adelazzi: We can submit it.

[00:21:44] adelazzi: When we submit it, every test, the solution is saved.

[00:21:48] adelazzi: This is changing the status of the challenge.

[00:21:58] Customer: Okay.

[00:21:58] adelazzi: So scenario of writing a code, see the terminal, testing the code is working.

[00:22:05] adelazzi: We need only— we need to add the feature of the VS Code.

[00:22:12] adelazzi: So there is some features are already working here: the login and logout, the create, everything is working also.

[00:22:22] Customer: Then the second feature is like I think an exercise.

[00:22:27] Customer: So you have some exercises here?

[00:22:31] adelazzi: Yeah, this prepared exercise.

[00:22:32] adelazzi: This exercise already in our database.

[00:22:35] Customer: Who can, who can see this exercise?

[00:22:38] adelazzi: This exercise, everyone, every user.

[00:22:44] Customer: Uh, okay, so why do I see them here?

[00:22:52] Customer: What is this page?

[00:22:54] adelazzi: This page is the front page.

[00:22:56] adelazzi: This is the new challenge, creating challenge here.

[00:23:00] adelazzi: You can see, you can see like the code which is we are created from initial way or the other user created.

[00:23:09] adelazzi: Maybe there is some user asking AI to create a bug.

[00:23:13] Customer: Sorry.

[00:23:14] adelazzi: Yeah.

[00:23:16] Customer: Oh, sorry for interrupting.

[00:23:18] Customer: So if you change the topic, what happens?

[00:23:22] adelazzi: For initially there is no topic.

[00:23:24] adelazzi: We have only one topic array and loop.

[00:23:27] adelazzi: We're going to add multiple topics here, the multiple difficulty and multiple language later.

[00:23:34] adelazzi: So if user— this is one of the scenarios— users using AI, the AI creating the debug— the bug, okay, the challenge.

[00:23:45] adelazzi: And give us those features and store it in the SQL.

[00:23:49] adelazzi: So if other user come again in some time, it's another user, new one, he come here to this form and try to, to use the existing exercises.

[00:24:04] adelazzi: He didn't— he don't need to create another one with AI.

[00:24:08] adelazzi: You want to see those exercises?

[00:24:10] Customer: Yeah, I see.

[00:24:12] Customer: Um, uh, what I'm confusing about is that, uh, you have topic difficulty and language, and-

[00:24:21] adelazzi: Yeah.

[00:24:23] Customer: they currently don't do anything, right?

[00:24:27] Customer: And what do they do?

[00:24:29] adelazzi: All of them are in, in, in loop.

[00:24:33] Customer: Oh nice.

[00:24:34] Customer: Okay, so these are filters, right?

[00:24:38] adelazzi: Yeah.

[00:24:39] Customer: Okay.

[00:24:40] adelazzi: For now we don't have any, uh, bug in dictionary.

[00:24:45] adelazzi: We have only in array and loop.

[00:24:47] adelazzi: The same thing for the medium.

[00:24:49] adelazzi: There is no medium.

[00:24:51] adelazzi: All of them are in easy way.

[00:24:53] Customer: Okay.

[00:24:54] Customer: And I also see describe the bug you want to practice at the top of the screen.

[00:24:59] adelazzi: This one?

[00:25:02] Customer: What is it?

[00:25:03] adelazzi: For research for one of the debugs.

[00:25:07] Customer: What do you mean?

[00:25:08] adelazzi: I search maybe for this negative.

[00:25:12] adelazzi: Sorry.

[00:25:16] adelazzi: He mentioned, yes, we have a debug in that topic.

[00:25:21] Customer: Why do I see all other exercises?

[00:25:23] Customer: Okay.

[00:25:29] adelazzi: So we need to remove all the other exercise, the duplication.

[00:25:33] adelazzi: It's—

[00:25:33] Customer: I mean, I mean, what is this for?

[00:25:36] adelazzi: Like, this for like for searching, because with the time we will have a long list.

[00:25:43] adelazzi: Okay, this is the filter, like maybe in one filter in this, those condition, we have a long list, maybe I don't know, 10 or more than 10 exercise.

[00:25:55] adelazzi: So he click here, asking for one.

[00:26:00] adelazzi: We need to find a way for, like, asking for and search for this.

[00:26:04] adelazzi: And when he asks for find exercise, it will go here.

[00:26:12] Customer: Uh, so where will it go?

[00:26:14] Customer: Missing class element.

[00:26:17] Customer: I don't quite get it.

[00:26:18] Customer: So this is search by name or what?

[00:26:22] adelazzi: This one?

[00:26:24] Customer: No, describe the bug you want to practice.

[00:26:27] Customer: This is like search by name, search exercise by name, by title, or what?

[00:26:33] adelazzi: It's by title.

[00:26:36] Customer: Okay, by title.

[00:26:38] adelazzi: Or no, and no, I know sometimes someone like he didn't have the real title, so even it's the same topic and the same bug, but he can't write the exact title for it.

[00:26:49] adelazzi: I know.

[00:26:54] Customer: Okay, so this is searching for an existing exercise, right?

[00:27:07] adelazzi: Yeah.

[00:27:08] Customer: Okay, so why is it above prepared exercises and AI generated?

[00:27:15] adelazzi: Above what?

[00:27:17] adelazzi: Ah yeah, why, why is it have those?

[00:27:23] Customer: It should move like, should be visible only in prepared exercises because—

[00:27:30] adelazzi: Ah, okay.

[00:27:31] Customer: I mean, I mean, it's one option.

[00:27:33] Customer: Uh, yeah, uh, or— Okay, currently I'm confusing by one thing.

[00:27:43] Customer: Here I see matched the duplicated result.

[00:27:48] adelazzi: Yeah.

[00:27:49] Customer: Below search.

[00:27:50] Customer: Yeah, matched the duplicated result.

[00:27:53] Customer: I don't see any exercises and I don't know like where to expect to see found exercises.

[00:28:00] Customer: This is one exercise, like this is an exact match.

[00:28:05] Customer: What if you remove like a result From the query.

[00:28:11] Customer: So, okay, for research, or you remove duplicated.

[00:28:15] Customer: Okay, okay, just the— what happened?

[00:28:19] adelazzi: There's no way.

[00:28:25] Customer: Yeah, uh, I mean, where should I see them, like in the sidebar or in the sidebar?

[00:28:33] adelazzi: Sidebar.

[00:28:33] Customer: Or below this search.

[00:28:36] adelazzi: Can you see my mouse?

[00:28:37] Customer: Yeah, I mean, I see here one exercise.

[00:28:40] Customer: If you have multiple exercises, how will they look like?

[00:28:44] Customer: Like, like here, like what, what you show me now, actually, or like cards on the right?

[00:28:52] Customer: The card on the right takes like too much space, I guess.

[00:28:56] adelazzi: Actually, we assume the user, when he want to search about the exercise, He already know the name of the exercise, the title of the exercise.

[00:29:06] Customer: Why would you know?

[00:29:08] adelazzi: So without scrolling here and there, he just came here and put it.

[00:29:13] adelazzi: Maybe some friends told him, I solved maybe this exercise, go searching it and try to solve it, and something like that.

[00:29:23] adelazzi: So he, he don't need like to scrolling and searching here, he just Give the title, find the exercise, the exercise is shown here, and start practice.

[00:29:37] Customer: Okay, but, um, if nobody told them and they don't remember, or they don't remember the exact name, and they type Like some matches should be found, like several exercises, and then you need to display all of them somehow.

[00:30:01] Customer: Where should they see them?

[00:30:04] adelazzi: Yeah, for now this function is just finding one, not a list.

[00:30:09] adelazzi: Yeah.

[00:30:10] adelazzi: So you suggest to, uh, giving the list here, not just one, it will be multiple ones here. uh, which is linked with this topic or this describe.

[00:30:28] Customer: Yeah, is that correct?

[00:30:30] Customer: So, um, I propose that search is only available for prepared exercises.

[00:30:41] adelazzi: Yeah, of course.

[00:30:43] Customer: Uh, and it's not available for AI Yeah, because you generate a fresh exercise.

[00:30:51] adelazzi: Yeah, that's, that's, that's wrong from us.

[00:30:54] adelazzi: It's logically, it's not showing if we are clicked on AI Generate.

[00:30:59] Customer: Yeah.

[00:30:59] Customer: So yeah, then, uh, okay, I think like what you show on the right is a convenient thing, like, like an exercise preview.

[00:31:12] Customer: Uh, but you should show it only when the user selects an exercise.

[00:31:18] Customer: So they, um—

[00:31:21] adelazzi: You mean this?

[00:31:22] adelazzi: You mean this side?

[00:31:23] Customer: Yeah.

[00:31:25] adelazzi: He is like, when he click on find, he already selected this one.

[00:31:30] adelazzi: So that's why it is showing here.

[00:31:33] Customer: Like I told you, like the, "the quarter case", because they don't remember the exact name, they, they type just uh, "the", okay, without other words.

[00:31:46] Customer: They have 3 results.

[00:31:48] Customer: Yeah.

[00:31:50] Customer: And then they should see a list somewhere.

[00:31:53] Customer: Yeah, maybe.

[00:31:54] Customer: I think you can keep the list like as it is now, like in the exercises section at the bottom of the screen right now.

[00:32:03] adelazzi: Um, yeah, that's right.

[00:32:05] Customer: But like And yeah, and here you will be able to show multiple results, and you should not select an exercise like, I mean, okay, if you want to select an exercise like by default, some of the exercises, then you should probably select like the first one, not the last one.

[00:32:32] Customer: Like the first one will be like the best match to what the user typed, for example.

[00:32:38] Customer: Then you can highlight it, select, like show it on the right.

[00:32:44] Customer: But if there are no results for the search, yeah, you should not— you should show nothing here on the right basically.

[00:32:55] Customer: Okay.

[00:32:56] Customer: Yeah, also I think I think you should move the, the search, like the input, even below the filters, like topic, difficulty, and language.

[00:33:09] adelazzi: This thing?

[00:33:10] Customer: Yeah, yeah, like even below, uh, lower, like just above exercises, so that the user can immediately see like the search results after they type something. in this input field.

[00:33:28] adelazzi: Okay.

[00:33:31] Customer: Um, and yeah, okay, this flow will be logical.

[00:33:38] Customer: Okay, and then they can start Praxis, uh, then they can open VS Code and solve something and somehow submit.

[00:33:50] adelazzi: Yeah, yeah.

[00:33:51] adelazzi: So, well, Right now we need to do the VS Code integration.

[00:33:59] adelazzi: Yeah.

[00:33:59] adelazzi: And create an extension.

[00:34:04] Customer: Okay, since I'm not sure how it will look like, like maybe VS Code embedded into your site, like it will just be in the middle, or it will take the whole— if you take the whole screen then they should be able to submit from the VS Code, like to not switch to the site.

[00:34:25] Customer: Um, so no, no run tests button on the site, but it should be somewhere in the VS Code.

[00:34:35] adelazzi: Okay, okay, we will find a solution.

[00:34:37] adelazzi: We will find a solution.

[00:34:39] adelazzi: We will test both of those ideas.

[00:34:41] adelazzi: One of them is like go to the site and with extension and so on.

[00:34:46] adelazzi: And the other thing is like trying to run the IDE, online IDE, inside the website.

[00:34:55] adelazzi: I'm gonna try both of them.

[00:34:57] Customer: Okay.

[00:34:58] adelazzi: To see which is the best solution.

[00:35:00] Customer: I mean, they're the same basically.

[00:35:02] Customer: Like either you run VS Code like desktop app or you open VS Code in the browser.

[00:35:09] Customer: Anyway, you connect by SSH Anyway, you somehow submit the solution from VS Code.

[00:35:15] adelazzi: Yeah, yeah, yeah.

[00:35:18] Customer: Okay,

[00:35:19] adelazzi: I think that's it.

[00:35:20] adelazzi: Thank you for your time.

[00:35:22] Customer: Uh, yeah, thank you for your work.

[00:35:25] adelazzi: Thank you.

[00:35:26] Customer: It's great to see some results.

[00:35:29] adelazzi: Thank you.

[00:35:30] adelazzi: How can I—

[00:35:30] Customer: Okay, yeah, just click stop.
