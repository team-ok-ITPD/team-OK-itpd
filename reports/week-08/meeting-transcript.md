# Meeting transcript

- **Date:** 2026-11-20
- **Participants:** @addelazzi, @UTKANOS-RIBA, @Danashi11, @qwxiae

[00:00:01] Speaker A: If you type, yeah, that's right. I think so. We have some issues with integrations parts.

[00:00:21] Speaker B: This live demo?

[00:00:22] Speaker A: Yes. It will go wrong. It will go wrong. So try. Yeah, yeah, yeah. This is my work. Okay, let's go. This is a teacher site. So here you have 4 basic uh pages, yeah? First is group. You're not assigned a group. The group is assigned by administrator to you. Mhm. So you can just open group, see the assignments, it applied, assigned, see the name, email, and when it's deadline, there will be a result and the suspicious mark.

[00:01:11] Speaker B: Uh, what's that?

[00:01:14] Speaker A: This is assignments assigned to this group. For example- To this

[00:01:17] Speaker B: group? To which one?

[00:01:19] Speaker A: Python A group.

[00:01:22] Speaker B: Did I see other groups?

[00:01:24] Speaker A: Yeah, Python B, Python

[00:01:28] Speaker B: A. Okay, we are in Python A.

[00:01:30] Speaker A: We are in Python A.

[00:01:31] Speaker B: All right, assignments with deadlines.

[00:01:34] Speaker A: Yeah, we have some deadline, we can close it. Before, we can export CSV, awaiting verification, no submission, not checked. Okay, so this is for This, yeah?

[00:01:51] Speaker B: Yep.

[00:01:51] Speaker A: Then, exercise catalog. This is public catalog. You can see all the exercises, maybe some of them yours, just yours. Some public, you can unpublish it. Some not public, private.

[00:02:12] Speaker B: Okay.

[00:02:13] Speaker A: You can open it. You can uh somehow edit it, yeah, and open it with VS Code to edit.

[00:02:36] Speaker B: Uh-huh. Okay, waiting.

[00:02:39] Speaker A: Main test. This is- so there is. You can somehow edit it here and uh submit. I didn't check the submission now, but it uh should be here. So you can uh edit it and submit to the system.

[00:03:06] Speaker B: Okay, what what did they say, the debug gym tests? Is it an extension or what?

[00:03:15] Speaker A: Yeah, there is an extension that-

[00:03:17] Speaker B: Is it your extension?

[00:03:19] Speaker A: Yeah, this is our extension.

[00:03:20] Speaker B: So it's pre-installed in VS Code when they open it?

[00:03:23] Speaker A: Yeah, that's that's how it worked before with Solanum.

[00:03:28] Speaker B: All right,

[00:03:30] Speaker A: uh, okay, so So it's it's about yours. Then that's uh what interesting.

[00:03:38] Speaker C: If you- What's the interesting thing?

[00:03:41] Speaker A: I will discuss it now. If you go to not your uh exercise. Okay, there should be-

[00:03:53] Speaker B: Assign it to your group.

[00:03:56] Speaker A: Yeah, where where it is? You only assign it to your group to create your own private- Yeah, so when you assign the not your application, not your exercise, it will uh create a new version, like a copy of this exercise, to avoid not needed version control system. Because if some unpublish the exercise. What would be with like the current assignments? What would be with like the teachers who use this exercise? So it will be created, and if it's somehow updated, there will be link in the description from which it is a copy.

[00:04:44] Speaker B: Okay,

[00:04:45] Speaker A: so

[00:04:46] Speaker B: reason one. How do I assign it to my group?

[00:04:51] Speaker A: Let's try. Create an exercise. No, that's not there. Let's go here. Let's go here. Let's assign exercise. Um. It's only yours, maybe. Let's check how it's called. Average of an empty list. Crashes. Go here, assign it here. So it will be fixed. Uh, there will be like uh options. I will fix it. There will be options like or in catalog to assign it directly.

[00:05:40] Speaker B: Mm-hmm.

[00:05:40] Speaker A: Or uh here to go to catalog to assign, or then in then option, two options. And to assign-

[00:05:52] Speaker B: Here which exercises do I see?

[00:05:56] Speaker A: That's all exercises, so it's not good because it will be a really big number of exercises here, so it's all. Uh I think We will we will put there only private, maybe. Or not. We go we go to uh we'll do it like this way. When you choose assign exercise, you'll go directly to exercise catalog and you can filter and you can check and uh from there you can Uh, view details and assign to which group. Okay?

[00:06:40] Speaker B: Um, okay.

[00:06:41] Speaker A: That's okay for you?

[00:06:42] Speaker B: Yep.

[00:06:43] Speaker A: Okay, then create exercises, two options. First, like, generate with agent. We can make it like sites like that, or with uh windows like to to change, like by hands or generated, and you will-

[00:07:01] Speaker B: Yeah, like tabs.

[00:07:04] Speaker A: Yeah, tabs, tabs. Or that way, it looks uh some pretty ugly. Yeah,

[00:07:09] Speaker B: yeah, like pretty much empty space.

[00:07:12] Speaker A: So we will make tabs. That's okay. Then prompt, language, uh, tests, submit. Generate and verify. Manage APK, it's personal if you need to, or if it's not here, it will be used uh in box. Uh generate and verify, and after that you can go to change it in VS Code. For now, without AI in VS Code. Then here. In prompt you can specify some environments, needs, for example, Leetchi or some libraries or dependencies and so on. Or you can upload the project, so you go with- it should be deleted, somehow it's still here. So- Project and upload the-

[00:08:18] Speaker B: what do I upload again? Can you scroll? Compress your project folder into a zip.

[00:08:23] Speaker A: Where, where, where? Yeah, to zip. The size starts- so you submit here the project itself and here a compose. Okay, then create. So we don't even have anything. To check it right now with you, but still it should work like that.

[00:08:48] Speaker B: Okay,

[00:08:49] Speaker C: so you finish your side?

[00:08:51] Speaker A: We will. There is some minor changes still.

[00:08:55] Speaker C: We're gonna go to the other role, which is student.

[00:08:59] Speaker B: Docker Compose, how do I know how to write it?

[00:09:03] Speaker A: Not write.

[00:09:04] Speaker B: Why is it Docker Compose? Okay, so what about Dockerfiles?

[00:09:16] Speaker A: Which files?

[00:09:17] Speaker B: There is Dockerfile, like, without space. Dockerfile. It's literally called like that. So it describes the container.

[00:09:26] Speaker A: Should it be in project or it it go only Dockerfile or Dockerfile, Docker Compose?

[00:09:37] Speaker B: That's a good question. Uh, what can you run on your server? Like a Docker Compose you can run, but like what about settings, like how much memory you allocate?

[00:09:53] Speaker C: It's in Dockerfile.

[00:09:55] Speaker B: No.

[00:09:55] Speaker C: Configuration.

[00:09:56] Speaker B: I'm talking about YAML. So here you can upload Docker Compose YAML file. There you can define services, uh like write how much memory each container will have. Um but like is it consistent with your backend server? Like how can you tell the teacher that this is too much memory? Like, are you going to check each Docker Compose file or not? And if they define several services, I think it's it's a hard task a bit.

[00:10:37] Speaker A: Okay.

[00:10:38] Speaker B: So I suggest to switch to just Dockerfile. So we run one container per task, okay? Not several interconnected containers.

[00:10:50] Speaker A: So just Dockerfile.

[00:10:51] Speaker B: Yes.

[00:10:52] Speaker A: So we just switch it to Dockerfile.

[00:10:56] Speaker B: Exactly.

[00:10:57] Speaker A: Okay.

[00:10:58] Speaker B: Uh, okay.

[00:11:00] Speaker A: What about submitting the project? Is it okay for you to submit the zip?

[00:11:07] Speaker B: Zip file. Uh, an alternative is to submit a link to a repo. It will download from the repo. Another one is to- about submitting, no other options really.

[00:11:28] Speaker C: Why we need zip?

[00:11:30] Speaker B: So like uncompressed files or what?

[00:11:33] Speaker A: Just files?

[00:11:34] Speaker C: Yeah, why we need it? The student will just directly use a VS Code and he working in our server.

[00:11:40] Speaker A: It will be easier to submit.

[00:11:44] Speaker B: So one other option is to run a Git server and they will push to the server. They can pull from that server, push.

[00:11:56] Speaker A: So there should be a button called VS Code, and inside VS Code he will push it.

[00:12:05] Speaker C: I have it.

[00:12:08] Speaker A: Why you have it in student site? Students cannot create an A project.

[00:12:13] Speaker C: He can create- no, not a project. He can create a bug which would be public bug.

[00:12:20] Speaker A: Oh yeah.

[00:12:21] Speaker C: For practicing.

[00:12:23] Speaker B: Students can't.

[00:12:24] Speaker C: Can.

[00:12:25] Speaker B: Cannot.

[00:12:26] Speaker C: You mentioned that he can, like for practicing.

[00:12:29] Speaker A: He cannot.

[00:12:29] Speaker B: For themselves only.

[00:12:31] Speaker C: For themselves only, yeah.

[00:12:32] Speaker A: Not public.

[00:12:33] Speaker B: But not to the- they can't add it to the public gallery.

[00:12:36] Speaker A: Cannot. Yeah.

[00:12:37] Speaker C: He cannot?

[00:12:38] Speaker B: Yes, they cannot.

[00:12:39] Speaker C: I add that to him. It's like an option. He can add it public or private.

[00:12:44] Speaker A: It's called only private for students.

[00:12:46] Speaker C: Why? What if the student-

[00:12:48] Speaker A: Because he can he can make it malicious file.

[00:12:51] Speaker B: Yeah,

[00:12:51] Speaker A: we don't trust students. Do you trust yourself?

[00:12:55] Speaker C: Yeah, I trust

[00:12:56] Speaker A: myself. I don't trust myself when I make some public. Like,

[00:13:00] Speaker C: okay,

[00:13:01] Speaker A: it's good, it's good, it's good.

[00:13:04] Speaker C: Something for stealing the information from the laptops?

[00:13:06] Speaker A: Yeah, suddenly by mistake my file can steal your money. It's not my fault, it's just a typo. So we don't trust students, just private.

[00:13:18] Speaker C: Okay, okay.

[00:13:19] Speaker A: And here we will remove all anything despite like the form and add the button go to Yeah,

[00:13:31] Speaker B: uh,

[00:13:32] Speaker A: we we will reuse your solution and we will see it now and reuse it somehow.

[00:13:40] Speaker B: Uh, I don't get what his solution is. Like, okay, here instead of uploading a project, I open VS Code.

[00:13:52] Speaker A: Yeah,

[00:13:53] Speaker B: I see some files.

[00:13:55] Speaker A: No.

[00:13:57] Speaker B: I think I should see a Dockerfile.

[00:14:01] Speaker A: When you submit it.

[00:14:02] Speaker B: No, I mean, I I want some scaffolding, like I don't want to write it from scratch. Okay. So I see the Dockerfile at least. Uh, Python files, and mainly main.py I see also. Uh, with the main function. No, maybe a test harness as well, just with some like placeholder function, okay, just with pass. Uh, yeah, so I see some scaffolding, like several files in VS Code, and then I can edit these files and save changes, okay, and the changes are saved on the server.

[00:14:49] Speaker A: Yes?

[00:14:50] Speaker B: So, uh, should I- What?

[00:14:56] Speaker C: The changes and tests, something like that?

[00:14:58] Speaker A: The submitting the-

[00:15:01] Speaker C: Submitting the exercise, not creating exercise.

[00:15:05] Speaker A: Creating exercise.

[00:15:06] Speaker B: So after editing- after editing files, what happens to those files? The student edited files.

[00:15:15] Speaker C: Yeah.

[00:15:17] Speaker B: Okay, now we have teacher. Teacher edits files. What, what next? Um, ideally there should be some versioning system, so there should be like, like Git for teacher.

[00:15:33] Speaker A: No, that's too much.

[00:15:35] Speaker B: What?

[00:15:36] Speaker C: What the hell?

[00:15:37] Speaker B: I mean, that's ideally. But like simpler, it's on on each save you just push to the server like the all changes, all files. If they didn't change, you don't push. So the server just stores the files.

[00:15:55] Speaker A: We will not make the versioning system. It's not for that. It's not the purpose of the system.

[00:16:03] Speaker B: Um,

[00:16:03] Speaker A: it's too hard. Such less money. Then is, uh, okay, I got the feedback for this side. We will simplify it, we will make tabs, we will make this, uh, in VS Code directly. Okay?

[00:16:19] Speaker B: Yes.

[00:16:20] Speaker A: Uh, with this part, you're good?

[00:16:24] Speaker B: Yes.

[00:16:25] Speaker A: From that you can assign.

[00:16:27] Speaker B: Oh, I'm kind of good. Uh, I don't like that there is like Several items in a row. I'm not sure if it's necessary, um, if it will be convenient to read.

[00:16:47] Speaker A: Okay, so we will make it like-

[00:16:50] Speaker B: What if it's a grid, some like table?

[00:16:54] Speaker A: We will make it like that.

[00:16:56] Speaker B: Will it work?

[00:16:57] Speaker A: This, then this description and there is actions, so it will be one. There will be another. Then you can open exercise, open it in VS Code, change something, unpublish it if you don't want to make it public no more, or publish it again.

[00:17:21] Speaker B: So can I unpublish from within exercise page?

[00:17:25] Speaker A: From this?

[00:17:26] Speaker B: Yeah.

[00:17:27] Speaker A: No.

[00:17:28] Speaker B: Why?

[00:17:28] Speaker A: Because there is an editing page. You save the details firstly and then publish.

[00:17:34] Speaker B: Okay.

[00:17:37] Speaker A: We cannot just make it publish despite of like save details because- and we cannot make it publish here because it can be mistake by by mistake publishing and it's not good because if it's up- if okay. So, there's- you're good with this?

[00:17:57] Speaker B: Uh, what if I have like 10 groups?

[00:18:03] Speaker A: Then you will be- you will have a-

[00:18:05] Speaker B: I will scroll. Okay, I will not search.

[00:18:07] Speaker A: No.

[00:18:08] Speaker B: Okay, for students, for students.

[00:18:11] Speaker A: You need search here?

[00:18:14] Speaker B: Um, I'm not sure. This works for now.

[00:18:20] Speaker C: Yeah,

[00:18:22] Speaker A: not not not not much.

[00:18:25] Speaker B: Still like 5 rows. Okay, it's okay. I don't expect there will be many more.

[00:18:30] Speaker C: For me, for the test, it is like 5, 10 maximum, I think.

[00:18:35] Speaker B: Yeah, uh, okay, 10, 10 groups, um, will be okay. First year Python morning group. Do groups have some descriptions or what?

[00:18:50] Speaker C: Some description?

[00:18:53] Speaker A: No. Ah, yes. First year Python morning group.

[00:18:58] Speaker B: First year. So are they added by admin or what?

[00:19:04] Speaker A: By admin only.

[00:19:06] Speaker C: Only admin.

[00:19:08] Speaker B: First year Python. Morning group.

[00:19:13] Speaker A: So there there should be there could be a timetable of lessons and something and something and the the the room this and and some guiding information but editable only for admins.

[00:19:30] Speaker B: Okay.

[00:19:31] Speaker A: Because because it says

[00:19:35] Speaker B: um. Okay, okay, so teachers don't need um to assign different descriptions to the same group, so maybe it's okay. Uh, all right, oh, exercise catalog. Search titles. Uh.

[00:20:09] Speaker A: There is your item.

[00:20:11] Speaker B: Yeah. Okay, public item, all accessible.

[00:20:17] Speaker A: My public?

[00:20:18] Speaker B: My public.

[00:20:20] Speaker A: Your

[00:20:21] Speaker B: public

[00:20:21] Speaker A: is public and private too. We should- Right.

[00:20:28] Speaker B: Private. Private. All accessible. My exercise is public. Uh, I am confused like about private here. So maybe you explain somewhere like what is private, what is public.

[00:20:49] Speaker A: You know what is private.

[00:20:55] Speaker B: I don't like-

[00:20:57] Speaker C: Private bug, it's mean like yours bug. There's no one can see it.

[00:21:02] Speaker A: That's-

[00:21:04] Speaker B: I know as a customer that we introduced this term like private.

[00:21:09] Speaker A: Okay, no, for customer it's obvious because you he see private, he see public, he see publish, he see unpublish on public exercise. So it's it's to think 2 seconds.

[00:21:25] Speaker B: Okay, alongside exercises shared by the community. Um, private, public, publish exercise. Okay, my exercises. Uh, all of them are mine.

[00:21:46] Speaker A: No, that's not filter. You shouldn't- you should put filter.

[00:21:50] Speaker B: Ah, it does not filter by default.

[00:21:52] Speaker A: Yeah.

[00:21:53] Speaker B: Okay, I have to click. Okay, I'm not sure.

[00:21:59] Speaker A: Okay, we will- that's okay, that's usability testing.

[00:22:03] Speaker B: Yeah. Um, okay, my exercises. Who is this exercise? No, no, no, it's not about filtering. So whose exercise is this?

[00:22:18] Speaker A: Some guy, some different

[00:22:22] Speaker C: professors.

[00:22:23] Speaker A: You you need to know?

[00:22:25] Speaker B: I want to know, like email or something.

[00:22:29] Speaker A: Okay.

[00:22:30] Speaker B: Who is the creator?

[00:22:32] Speaker A: Is it is it okay?

[00:22:34] Speaker C: No, do the full name, it's true.

[00:22:36] Speaker A: Just name. Okay.

[00:22:40] Speaker B: Just name. Um. So you store names, you don't store emails? We

[00:22:47] Speaker A: store emails, but it's not like-

[00:22:50] Speaker C: like email for contact. Okay.

[00:22:53] Speaker B: They don't have usernames like on Codeforces. You use like names, right?

[00:22:59] Speaker C: Yeah.

[00:22:59] Speaker A: Yeah.

[00:23:00] Speaker B: Um. Okay, okay, let's, let's use the name.

[00:23:06] Speaker A: So

[00:23:07] Speaker B: I know this guy by this name. No, maybe you'll be-

[00:23:12] Speaker A: you know your uh teacher, you know the teacher you know, but if you want to spam somehow some guy you don't like, you don't need to- you, you must not have the access to the personal information of the teachers.

[00:23:32] Speaker C: Really? Sounds good.

[00:23:34] Speaker B: Students don't need to have this access?

[00:23:36] Speaker A: Students need to have it, but it's, uh, managed not by our side.

[00:23:43] Speaker B: Um, okay, I can agree. Uh, all right,

[00:23:51] Speaker A: so I write- I'm writing catalog UI.

[00:23:56] Speaker B: Details.

[00:23:58] Speaker C: The item.

[00:24:00] Speaker A: UI. Then filter.

[00:24:06] Speaker B: Here is my exercise.

[00:24:07] Speaker A: Private two tabs. Then explain what is private. Then I need to put names of creator, owner, of box owner. Okay, then for groups we have all all good.

[00:24:37] Speaker B: No,

[00:24:39] Speaker A: what is-

[00:24:42] Speaker B: I think we should introduce courses. So a group belongs to a course.

[00:24:50] Speaker A: That's new requirement. That's really expensive to add it now.

[00:24:57] Speaker B: Let's discuss it. Why is it expensive?

[00:25:03] Speaker A: Because we have a lot of work still because of requirements changed previously.

[00:25:08] Speaker B: Okay.

[00:25:09] Speaker A: And we have not much, much, much time. And we not paid for that.

[00:25:13] Speaker C: That means new table, new relation between tables, new UI/UX.

[00:25:19] Speaker B: Okay.

[00:25:20] Speaker A: So we put only groups because the courses managed by Moodle, not by us, because we not Moodle. We we not Moodle. Yes? If we will add courses, the only need to get Moodle, we the grades. That's it. And we model.

[00:25:49] Speaker B: Okay, the course name can go here.

[00:25:52] Speaker A: And it could be in description.

[00:25:54] Speaker B: Yeah, I will not be confused like which course.

[00:25:59] Speaker A: Description is text. Description is could be like different.

[00:26:04] Speaker C: Text named course, something like that. Yeah, without any relation, without anything. Add a new field or attribute to this class,

[00:26:13] Speaker B: like a description.

[00:26:14] Speaker C: Yeah,

[00:26:15] Speaker B: with just

[00:26:17] Speaker C: so small a course.

[00:26:18] Speaker B: Okay, if it works, then yes, please add. Um,

[00:26:25] Speaker A: I guess, but I don't know.

[00:26:27] Speaker C: Why are you doing that?

[00:26:28] Speaker A: Yeah, we need only description and all needed information. goes in description. That's it.

[00:26:34] Speaker C: No, he means-

[00:26:35] Speaker A: Admins know what teachers need to know.

[00:26:39] Speaker B: I just wonder-

[00:26:42] Speaker C: You need to highlight, you want to highlight like the course.

[00:26:44] Speaker B: Yeah, how will admin know what teachers want?

[00:26:48] Speaker A: Because they work it together, they know.

[00:26:51] Speaker B: I have no idea who the admin of Moodle is.

[00:26:55] Speaker A: But suddenly they know what you know, what what you need to know. You need to know where you have the lecture.

[00:27:03] Speaker B: Yeah, they know my course.

[00:27:04] Speaker A: Yeah.

[00:27:05] Speaker B: Okay. But like they don't know the uh the schedule of the group maybe. Like why call it morning group? I mean if they could guess the course name here, they they sure know it because they know the groups, okay? And groups belong to courses. Groups have courses. And I am on the course, I am a teacher. So if they put just the course, they will not need to invent the format of this field of the description.

[00:27:40] Speaker A: So we will change the name of group to the name of course. We will check on one entity.

[00:27:47] Speaker B: Yes.

[00:27:48] Speaker A: Groups to courses.

[00:27:50] Speaker B: Kind of, yes.

[00:27:52] Speaker A: Okay, that's not that's not difficult, we just rename it.

[00:27:58] Speaker B: Uh, I mean, you don't change the group to course, you just add the field like which course the group belongs to, just another table.

[00:28:07] Speaker A: Okay, just add this text field without any relation.

[00:28:11] Speaker B: No, the relation is course belong uh group belongs to Of course.

[00:28:16] Speaker A: So it's new relation. Why do we need this?

[00:28:21] Speaker B: Because you need description.

[00:28:23] Speaker A: Okay, we have description.

[00:28:28] Speaker B: But where do you get it? Like,

[00:28:30] Speaker A: the admin should provide it.

[00:28:32] Speaker B: Okay, manually.

[00:28:34] Speaker C: Okay,

[00:28:34] Speaker B: and right,

[00:28:35] Speaker C: you're gonna see it, you're gonna see it, we're gonna show you the admin side.

[00:28:38] Speaker B: Okay, you tell, you tell admin like what to write Because they can write anything. If they don't write the course, it will be inconvenient for me as a teacher. So they write the course name.

[00:28:51] Speaker A: Yeah.

[00:28:52] Speaker B: Okay.

[00:28:54] Speaker A: I say like, then, then, okay, I agree. All needed information in description.

[00:28:58] Speaker B: All needed, yeah, okay. If you can specify, like, I need the course name first. And that should be like something at the start of this description. Everything else, okay, um, can go afterwards. Okay. Uh.

[00:29:21] Speaker C: Anything is ready with the professor's side?

[00:29:25] Speaker B: Let me check. Okay, assignments, week 1, loops, active. I would prefer a table here. Like this is second column, the blind shark. Okay, weak one loops. Some skip to the last item. Um, fix total so it adds every number, don't change the function name. So this is what students see, or what?

[00:29:57] Speaker A: Yes.

[00:30:01] Speaker B: I mean this thing, okay. Active status, deadline optional. Okay, I can set the deadline, save. Close assignment. Okay, opens the result table. What do you mean opens the result table? What is this?

[00:30:19] Speaker A: The- it's below. Below.

[00:30:23] Speaker B: Student results.

[00:30:25] Speaker A: Yes.

[00:30:25] Speaker B: Okay, opens to whom? What does it mean opens?

[00:30:30] Speaker A: You said that you need to check the suspicious after the alignment.

[00:30:36] Speaker B: Yes.

[00:30:37] Speaker A: So it opens the results. You have a waiting verification status. So, and that's it. So try to close this.

[00:30:52] Speaker B: I closed. Okay.

[00:30:54] Speaker A: You didn't close. Go up.

[00:30:58] Speaker B: This older assignment is shared with several groups.

[00:31:02] Speaker A: This older assignment is shared with different- ah, several groups.

[00:31:09] Speaker B: Okay, so was there some change in the server logic or what? What is it about? Why is it older?

[00:31:20] Speaker A: Because its deadline is already passed.

[00:31:25] Speaker B: Older than what? Uh, okay, okay. I set the deadline for, um, 21st of November. Okay, today, tomorrow. Um, I save the deadline. This older assignment shares a deadline across groups. Which groups?

[00:31:53] Speaker A: Different groups. Okay, I'll note it here.

[00:32:00] Speaker B: Save deadline clicked. Close assignment. This older assignment is shared with several groups. So I opened it for the Python A group. Yeah, okay, open a group, and then I learned that it's shared. I can't close it for the Python A group, so I can't have separate deadlines for each group.

[00:32:31] Speaker A: That's not like that.

[00:32:35] Speaker B: Okay, uh, okay, so how do I- um, yeah, so I need another assignment that is not shared with several groups, and then I can close it. So I- or I I can just- or are they all shared? If they're all shared, then I need to create a new exercise. Okay, I am creating the form. Medium, rare, okay. Solution code.

[00:33:24] Speaker A: That should be deleted.

[00:33:25] Speaker B: Yeah. Okay, it- we don't limit which files are uploaded.

[00:33:37] Speaker A: Yes.

[00:33:38] Speaker B: File types, I mean. Text files. Okay, anyway, it will change entry file path to the file containing um this thing. Okay. And then compose file. Okay. No file uploaded, valid zip containing.

[00:34:22] Speaker A: We not have some.

[00:34:24] Speaker B: Can I unassign exercise? Um, so I assigned it to Group A. Uh, I can't unassign it. OK, does the agent wave work? Because-

[00:34:49] Speaker A: Not yet, because we have no token.

[00:34:55] Speaker B: OK, do you need the token?

[00:34:56] Speaker A: Yes.

[00:34:58] Speaker B: OK, I will provide the token. Wave, uh, create. Ah, I have other exercises, but which of them are not assigned? Anyway. Okay, this exercise is assigned to a single team, I guess. Close assignment.

[00:35:33] Speaker A: So we need assignment- we need assignment of the exercise to every group separately.

[00:35:43] Speaker B: Yeah. And unassign. Okay, so I closed. Results are now available. How did I close it? How did it look? Okay.

[00:36:05] Speaker A: It's closed.

[00:36:07] Speaker B: Can I unclose? No.

[00:36:11] Speaker A: If you close, then it should be verified, should be checked, and that should be so closed forever. You can assign the same exercise another time, but you you cannot unclose, open again. You cannot.

[00:36:29] Speaker B: Yeah, I saw. Okay. I don't know if I want this.

[00:36:37] Speaker A: No, you don't want this.

[00:36:41] Speaker B: Why don't I want this?

[00:36:42] Speaker A: Because it's uh constrained. You don't need to reopen exercises. Because uh it would somehow finalizing the solutions and then it should be un-finalizing it. It should be notified that they're reopened and that's that's not possible.

[00:37:09] Speaker B: Um. But GitHub has archive and unarchive.

[00:37:15] Speaker A: That's different. That's soft delete.

[00:37:26] Speaker B: Okay, why why can I need to unclose? Okay, what does close do? It opens the table. I can check. Uh, can I want to check while the assignment is still open, like for some guy. Can I check like what some guy submitted before closing the exercise?

[00:37:55] Speaker A: I hope so.

[00:37:56] Speaker B: Okay. Uh, what else do I want from this? No submission, not checked, status change. Not, but it should change only after the final check. Um, okay, seems like, yeah, I don't need anything else. I can, so after closing, I don't need to unclose. Okay, maybe like the, uh, I can misclick and close it by accident.

[00:38:37] Speaker A: Then we need uh- You didn't ask me.

[00:38:39] Speaker B: Yeah. Like something, a model. Uh but anyway, student results, export CSV. Uh so I got a CSV. Sorry for downloading here. Um. And- oh wow, it works. Tests passed. Tests total. Verification. No, no submission. Ah, okay, yeah. Review not checked. Where is it? Review notes. Standard. Okay. Um, tests passed, test total. Yeah, I think everyone has own rules of how to interpret this number into grade. So no need for some grade column and formulas. Okay, and one time I just-

[00:39:45] Speaker A: We add grades in courses, we will become Moodle- We don't need Moodle.

[00:39:53] Speaker B: Um, well, yes. One time we-

[00:39:58] Speaker A: Maybe we can just delete everything else, we leave courses and grades and leave Moodle as is. Okay. Because firstly it started as like the platform to track training for everyone, not for university students. Then it became the platform for teachers and students.

[00:40:24] Speaker B: Yes.

[00:40:26] Speaker A: And then it became like groups.

[00:40:32] Speaker B: I-

[00:40:33] Speaker A: And that that says like pretty hard changed requirements. If we would like to- if we would be If you build a BVS in the beginning, then you should double pay now or triple pay.

[00:40:52] Speaker B: Yes, but we are agile people and we are at the university.

[00:41:01] Speaker A: No, if if you're talking like about the customer side, customer should triple pay in that case. Because of the BBS, like if you build a breakdown of work system, breakdown of work system, um we mentioned everything we told in the first session.

[00:41:18] Speaker B: If customer, if you build a WBS, um you wouldn't build it at the start. I think you would use waterfall or something like that. By now only you will have a WBS because only by now you have clarified the requirements. So I'm not sure if like you will start building before you clarify all the requirements. Is it your intention to clarify everything?

[00:41:51] Speaker A: We clarified it.

[00:41:52] Speaker B: Or is your intention to get more money from the customer by doing what they ask?

[00:41:57] Speaker A: We clarified it.

[00:41:59] Speaker B: Yes.

[00:41:59] Speaker A: The first session as uh the system for everyone who started to programming and wants to train the bug solving, not for students and not for university and not for teachers.

[00:42:15] Speaker B: Okay.

[00:42:15] Speaker A: And without like creating bugs. Yeah, creating bugs, it is, it was a great thing. There was no catalog. That was just create bug, train, that's okay, your score is 6/6.

[00:42:30] Speaker B: Right. Uh. Okay.

[00:42:37] Speaker A: So it's not our fault.

[00:42:42] Speaker B: It's not the fault, it's all right, it's like the process.

[00:42:47] Speaker A: It would be a good process if the requirements It's like not changed, but like fine. We've gone in way in a way of prototyping. Yes?

[00:42:58] Speaker B: Yes.

[00:43:00] Speaker A: So if we prototype it uh and then we show it, you will say like this, we need to add it, we need to remove it, okay. But now we show you first prototype, you change the half of it. Like, not the- you didn't like the UI or design, or like this should be that limiting, or yeah, but you change the, the goal, the system, and the goal, the, uh, like customers, the clients, you change the, like, this, the thought itself.

[00:43:39] Speaker B: Yes, yes.

[00:43:40] Speaker C: And make it more complicated.

[00:43:43] Speaker A: Yeah, in the real world it it it would be cheaper paid.

[00:43:47] Speaker B: I agree, but it will not be paid at all um unless you sign some contract with the customer, like correct and complete requirements.

[00:43:59] Speaker A: That's what I'm talking about.

[00:44:00] Speaker B: Yeah, but we did not- Yes,

[00:44:05] Speaker A: that's okay, I understand, but We're talking about real work. We we don't we will we would not stop we we would not start make something until it's signed.

[00:44:18] Speaker B: Yes.

[00:44:19] Speaker A: So,

[00:44:20] Speaker B: so

[00:44:20] Speaker A: if it's signed, we will do that what's signed.

[00:44:23] Speaker C: Yeah.

[00:44:24] Speaker B: Yes, and if if a customer asks for extra, you will charge extra.

[00:44:29] Speaker A: Yes.

[00:44:29] Speaker C: Yeah.

[00:44:30] Speaker B: Okay. Great. Um. And now your only way to go is to just discuss what you prioritize, how you prioritize, like what you do, what you don't have time to do in this project.

[00:44:56] Speaker A: Okay.

[00:44:58] Speaker B: One time agent review is queued. It starts automatically when a generation key is available. Okay, there is no built-in key, there is no teacher's key. Whose key is used?

[00:45:11] Speaker A: If there is no teacher's key, then it's built-in key.

[00:45:16] Speaker B: Okay, okay. Can the teacher change that?

[00:45:20] Speaker A: Yes, you can delete the key from the settings or your pad.

[00:45:26] Speaker B: Okay, it would be nice to make a toggle, like which key to use.

[00:45:31] Speaker C: By the way, the students also can add this key.

[00:45:35] Speaker B: Okay.

[00:45:36] Speaker C: API keys.

[00:45:37] Speaker B: For generating, yeah. Great. The agent checks all submissions. Uh, okay. Findings are advisory and need your review. How can you check? The table opened, I can't change the status.

[00:45:57] Speaker C: Check what?

[00:45:58] Speaker B: Status, not status, check submission, mark it as checked.

[00:46:04] Speaker C: It's coming automatically. Who gonna check the submission?

[00:46:11] Speaker B: So the agent runs, then the review status changes, and then I can We check because findings are advisable.

[00:46:22] Speaker A: Yes.

[00:46:23] Speaker B: Okay. So I can't check before the agent runs. Okay.

[00:46:30] Speaker C: Because it's kind of automatically when you submit the agent run.

[00:46:34] Speaker A: No, we talked about-

[00:46:37] Speaker C: Yeah, you mean after deadline.

[00:46:40] Speaker B: Uh, yes. Um, okay, the only problem where I get can get stuck is that agent fails and I need to check manually. Like we don't have access to OpenRouter anymore, for example. Um, maybe in this case, like when the agent fails, I check manually. So I can change the status manually. Um, okay, then I see those guys. I don't see their submissions. There are no submissions, therefore I don't see- uh, okay, I I think I see links to submissions in another column because this one is about tests passed out of total. Okay. Create exercise. You have looked at it. Tabs. Uh, your API key. Choose the credentials. Leave it empty to use the platform default. Uh, personal API key. Okay, where will it send requests? You should provide setting for endpoint, I guess.

[00:48:00] Speaker C: Endpoint?

[00:48:02] Speaker B: Each LLM provider has own endpoint to send requests to. If I only provide API key, you don't know where to send requests to.

[00:48:13] Speaker C: Yeah. Okay. It's not only API key.

[00:48:18] Speaker B: Hmm?

[00:48:19] Speaker C: It's not only API key. Yeah.

[00:48:22] Speaker B: Keep your key private. Uh, never displayed again. Save a new key to replace your saved empty field. Use the platform default. Keys are encrypted, address never displayed again. Okay. Save credentials saved. Bam. Your workspace. Okay. Into places. What is workspace? Um.

[00:48:52] Speaker C: The place where there is the most bugs from you.

[00:48:55] Speaker A: Это где ты работаешь? No, from where you logged. You logged as.

[00:49:02] Speaker B: Okay, I logged as. Okay. Uh, build, assign, review. Uh. Okay, I don't understand this.

[00:49:17] Speaker A: That's AI-generated motivation.

[00:49:21] Speaker B: Yeah, because I already have this. Okay, to assign group, 7 students, 5 your exercises, create new exercise. Um, maybe like clicking here should bring me to my exercises. Show, okay, and I see my exercise. Okay, I can- so teacher side is all right. So as a student, can I submit or I can't?

[00:49:51] Speaker C: Submit what?

[00:49:52] Speaker B: Solution. And it gets checked and I see verdict or not?

[00:49:59] Speaker C: What?

[00:50:00] Speaker B: Right now, like, as a student,

[00:50:04] Speaker C: yeah,

[00:50:04] Speaker B: I have an exercise.

[00:50:05] Speaker C: Yeah,

[00:50:06] Speaker B: can I solve it, submit, and get verdict like that.

[00:50:10] Speaker C: The server group, like check the your-

[00:50:14] Speaker B: Yes.

[00:50:14] Speaker C: Yeah.

[00:50:16] Speaker B: Okay.

[00:50:16] Speaker C: From the tests.

[00:50:19] Speaker B: Can you demonstrate this?

[00:50:22] Speaker C: That's mean we finish with the purpose, yeah?

[00:50:24] Speaker B: Yeah.

[00:50:27] Speaker C: Can I go?

[00:50:29] Speaker A: Guys?

[00:50:30] Speaker B: Um,

[00:50:31] Speaker C: I think yeah, you finished your work.

[00:50:35] Speaker A: I hope you find my side.

[00:50:38] Speaker C: Okay. Wait, I'm gonna change this. We're dealing with a student. This is an example from one of the assignments.

[00:51:04] Speaker B: I'm into groups. One assignment to graded submissions. Uh, recent grades. Grade. Grade? What is grade?

[00:51:16] Speaker C: From professor. I'll give him the grade of this uh assignment.

[00:51:25] Speaker B: Professor didn't give the grade.

[00:51:28] Speaker C: Yeah, it's missing. It's gonna complete from there and there.

[00:51:32] Speaker B: So

[00:51:32] Speaker C: each assignment have a grade.

[00:51:35] Speaker B: Okay, so you're building model.

[00:51:42] Speaker C: Something like that.

[00:51:47] Speaker B: Then let's put grade into the CSV that professor Downloads.

[00:51:53] Speaker C: Yeah, that's gonna be okay. And this will be like from email of student and the grade directly.

[00:51:59] Speaker B: Yeah. Okay, assignment week 4 lists bug Python medium. By uh all assignments week 4. Okay, I uh instructions, think about duplicates. As well. Second largest returns the largest. Okay, instructions, buggy code. What is this?

[00:52:25] Speaker C: This is the side, the bug.

[00:52:30] Speaker B: Okay.

[00:52:31] Speaker C: An example from the bug.

[00:52:32] Speaker B: An example from the bug?

[00:52:34] Speaker C: Yeah.

[00:52:34] Speaker B: What do you mean?

[00:52:35] Speaker C: It's like, this is the code you need like to fix it.

[00:52:39] Speaker B: Okay.

[00:52:39] Speaker C: Yeah.

[00:52:40] Speaker B: So when I solve this bug, I see this code.

[00:52:44] Speaker C: No, it's not solving. When you wanna solve this bug, you go and use the VS Code. This is only the details about the bug.

[00:52:52] Speaker B: Uh,

[00:52:54] Speaker C: the deadline, the professor who assigned the bug, your group.

[00:53:00] Speaker B: Okay, uh, I don't understand this.

[00:53:06] Speaker C: This is the code you need to

[00:53:09] Speaker B: I can't edit it here.

[00:53:11] Speaker C: No, you can't edit. You use VS Code. So you go into the solve.

[00:53:15] Speaker B: Yes.

[00:53:17] Speaker C: Click on Open in VS Code.

[00:53:20] Speaker B: Open your own VS Code.

[00:53:22] Speaker C: Yeah.

[00:53:24] Speaker B: Okay, open VS Code. Open in VS Code. I think the phrasing should change because I don't open my VS Code.

[00:53:32] Speaker C: We're gonna add this as Okay. SSH key, so that's why-

[00:53:36] Speaker B: The bug is in main.py. Click test in the status bar to run the- okay, find the mistake, click submit, server checks it by running the test. Best checked submission is one that counts. Um, this code keeps your changes between visits. Starting it can take a few seconds. Okay, task.

[00:54:05] Speaker C: Here we are opening the online VS Code in our server. So yeah, you can see it's here.

[00:54:10] Speaker B: Okay. Uh, I see localhost, so it will be like VM IP address.

[00:54:22] Speaker C: Yeah, yeah.

[00:54:24] Speaker B: Okay. So close, and then back is here. I see the code.

[00:54:35] Speaker C: Yeah,

[00:54:35] Speaker B: I see test. Okay, I see test submit. Also I see timeline.

[00:54:42] Speaker C: Those, uh, we can say default, by default is in VS Code server.

[00:54:47] Speaker B: Ah, okay.

[00:54:49] Speaker C: This is our-

[00:54:50] Speaker B: Okay, this is your

[00:54:52] Speaker C: Yeah.

[00:54:52] Speaker B: Fix bug, run the tests if it has any, then submit. Um, okay, let's try a test. Tests, 2 failed. Which failed?

[00:55:06] Speaker C: Those.

[00:55:09] Speaker B: Uh-huh. Okay. Assertion error. Okay. Test with duplicates. Um. Okay. I can run again. Test 1 failed. Okay. Can I run them together again?

[00:55:35] Speaker C: Yeah, there. That's all.

[00:55:39] Speaker B: Um. Is it- Amount of tests failed or number, like number 1, number 2?

[00:55:48] Speaker C: Number 1, number 2, number 3. It's like the count.

[00:55:57] Speaker B: Okay, close the chat.

[00:56:03] Speaker C: This is the test file. It's not the main debug.

[00:56:08] Speaker B: Yes.

[00:56:08] Speaker C: The bug is there. Yeah.

[00:56:10] Speaker B: Okay. Launch your song, settings. Okay. So uh if I have- oh yeah.

[00:56:24] Speaker C: You want to fix it?

[00:56:26] Speaker B: For example, I forgot where the status- where where I can click the test to run test.

[00:56:36] Speaker C: Yeah.

[00:56:37] Speaker B: Um, and I want to go back to see the instructions. Okay, I can see them. And I can return to VS Code, and it will save the changes, I promise. Um, okay. OK, it returned a promise and it's fulfilled.

[00:57:07] Speaker C: The keyboard does not work. Use the second one.

[00:57:11] Speaker B: Oh, it works somehow. OK. Um, what else? Submit. If I click Submit- Maybe it would be nice to- where is status bar- to explain that it's in the extension.

[00:57:34] Speaker C: Okay.

[00:57:34] Speaker B: Like somehow.

[00:57:35] Speaker C: Okay.

[00:57:38] Speaker B: I I may not be able to see it even.

[00:57:42] Speaker C: The extension?

[00:57:43] Speaker B: Yeah. Like why is it not a separate uh icon? Like it's- It's inside the Explorer. Like this would be, I think, a bit more like yeah convenient, but like use another icon.

[00:58:02] Speaker C: Okay.

[00:58:03] Speaker B: Um. I mean, I can understand the motivation, maybe like everything in one place, like files, actions with this files.

[00:58:14] Speaker C: Yeah, okay.

[00:58:16] Speaker B: Um, but I think this way it will be more discoverable.

[00:58:22] Speaker C: Okay, so it's on its own page.

[00:58:25] Speaker B: Okay, or or yeah, or at least just write the name of the extension, like what to look at, like where to click, like click Explorer, uh click Debug Gym Tests, like open Debug Gym Tests, click Test or Submit. As a user, I won't get stuck. Okay. Uh, then we submit without fixing. Tests to failed. So they failed on the server or where? Uh, anyway, doesn't matter.

[00:59:15] Speaker C: This is the problem. We are working on the server. Everything is on the server.

[00:59:18] Speaker B: Okay, okay. Uh, test second largest. Didn't even get the idea of the problem. Uh, second largest.

[00:59:32] Speaker C: The problem is.

[00:59:36] Speaker B: Second largest. Really?

[00:59:39] Speaker C: Or is second largest return?

[00:59:42] Speaker B: Like 9 is the first largest, 5 is the second. Okay. Uh like not -1, but -2, I guess.

[00:59:55] Speaker C: Yeah. Because it's sorted.

[00:59:58] Speaker B: But what if there is only one element.

[01:00:01] Speaker C: Which one element?

[01:00:03] Speaker B: Like only one element in the list. Or you guarantee that there is at least two. Ah, yeah, second largest, yeah. In this case, there is at least two elements in the list. Uh, okay, and also like duplicates. I don't remember, like set or something.

[01:00:27] Speaker C: Yeah, for duplicate?

[01:00:29] Speaker B: Um, yeah. Maybe- maybe again list? I don't know.

[01:00:44] Speaker C: Run test.

[01:00:47] Speaker B: Okay.

[01:00:48] Speaker C: That's right.

[01:00:50] Speaker B: And what is the output? What did my program print? How do I see? Can I run it in the-

[01:00:58] Speaker C: Yeah, you can run it. If you put main, Python main. As I mentioned, my keyboard is not working.

[01:01:07] Speaker B: Yeah, yeah.

[01:01:10] Speaker C: Okay. That's the one.

[01:01:14] Speaker B: Okay, because

[01:01:16] Speaker C: you don't have

[01:01:17] Speaker B: anything, so-

[01:01:18] Speaker C: Try to print. Use the second keyboard.

[01:01:21] Speaker B: Yeah. Um. Tiny second. Or just okay. Um. Uh and I I did not see the test, but I You can see it here. If I, for example, take this one and put it here, yeah,

[01:01:55] Speaker C: by this,

[01:02:07] Speaker B: I should run my Okay. Also should return a print. Okay. How can I go to the end of it?

[01:02:29] Speaker C: That's what it is,

[01:02:31] Speaker B: yeah. Okay. Okay, now I see the output.

[01:02:37] Speaker C: It's 3?

[01:02:40] Speaker B: Yeah, but it's it's wrong. Uh. Okay, we- return a new list containing all items from the- Unordered collection, but this is ordered. Okay, unique elements.

[01:03:14] Speaker C: It's sorted, I think. It's enough. Change the number 1 to 2. If I change number-

[01:03:24] Speaker B: What? What?

[01:03:25] Speaker C: No, remove set and list.

[01:03:28] Speaker B: All right, but what about- okay, in this case there are no duplicates and we're testing just the submission. Okay, now one test passing, another one-

[01:03:45] Speaker C: The second one is failing because

[01:03:47] Speaker B: it has

[01:03:47] Speaker C: duplicates.

[01:03:49] Speaker B: So if we just Commented out, what happens?

[01:03:56] Speaker C: It will be passed because you commented.

[01:03:59] Speaker B: Yeah, and if I submit it, where do I submit it?

[01:04:04] Speaker C: You can submit.

[01:04:06] Speaker B: Your fix was not submitted. The debug server could not be reached. Okay, um, I don't know why.

[01:04:17] Speaker C: Try it again. Try this out. Do the test, the whole test, not just one. No, no, no, no, like that. Click in here.

[01:04:26] Speaker B: Test 1 passed. Okay.

[01:04:35] Speaker C: Because what I what I did in the flow, it's me, this test is yours, but we have another file which has a lot of tests.

[01:04:42] Speaker B: Yes, yes.

[01:04:43] Speaker C: So that's me.

[01:04:44] Speaker B: Uh, so my program should fail your tests, but for this it should be like submitted, but it did not get submitted. Okay. Um, we can't we can't proceed with this scenario, I guess. Okay. Yeah. Is there a fix for this like right now or?

[01:05:09] Speaker C: Uh.

[01:05:11] Speaker B: Maybe this- can this be a problem? Like something was run on the server and it- no, it just could not be reached. Okay. In this case, we should check connection.

[01:05:31] Speaker C: Yeah, we need to make- we need to accept all the submissions.

[01:05:37] Speaker B: So after- did you check with with some student here already? Like how how does it look like after they submitted?

[01:05:46] Speaker C: After submission, go to the list of the assignment. This one.

[01:05:53] Speaker B: Hmm, okay, graded, grade, easy, deadline, yeah.

[01:06:00] Speaker C: If you miss it.

[01:06:00] Speaker B: Missed deadline. To do, okay. Uh, this assignment is closed, the deadline, new submissions are not accepted, okay. This is informative. Uh, okay, I see the code. So if the code is like 300 lines long-

[01:06:21] Speaker C: That's not solution, yeah.

[01:06:23] Speaker B: Yeah, this should not be shown here.

[01:06:26] Speaker C: Okay.

[01:06:28] Speaker B: Uh, this can be even comments in the file. Okay, status, test, grade, feedback. Okay, where can I see my submission? Um, this is

[01:06:46] Speaker C: submission. This is the code.

[01:06:49] Speaker B: Ah, this is the code.

[01:06:50] Speaker C: Yeah,

[01:06:50] Speaker B: so I can't open it in VS Code.

[01:06:53] Speaker C: You are doing the small one. Oh, you can't open the VS Code, so you wanna- yeah, you can.

[01:06:59] Speaker B: Or can I? Oh, nice, I can. Can I?

[01:07:04] Speaker C: Not in VS Code.

[01:07:06] Speaker B: So it's in VS Code. No verified submission yet. This work is closed, VS Code is not offered. Your last code is below. I think I should be able to see in VS Code but not submit.

[01:07:18] Speaker C: We can edit on it, like, so we make him see the code in VS Code, but we disable our uh extension. Or maybe don't accept it from the backend because we like we can use our extension for submit or something like that.

[01:07:35] Speaker B: They don't, they they can't submit, like, if they, okay, so they can just see the code. Um, your last submission, yeah. Okay, here will be like list of submissions, or I don't know.

[01:07:54] Speaker C: List of submissions for what? List of students, so he see only his submission.

[01:08:02] Speaker B: Yeah, I mean, I I see submissions here.

[01:08:05] Speaker C: Yeah.

[01:08:06] Speaker B: All submissions.

[01:08:07] Speaker C: This is like-

[01:08:08] Speaker B: And then I see view my code. And here, last submission. So I can see only one submission.

[01:08:14] Speaker C: Here?

[01:08:14] Speaker B: Yeah.

[01:08:15] Speaker C: The last one. And your submission doesn't mean the history. Like, you submit the first time and and it's not correct, you submit the next time. From misclicking or something like that.

[01:08:26] Speaker B: Yes, but why not see submission here? Yeah, like tracking history of submissions. What? Tests?

[01:08:37] Speaker C: You mean this one, the tests?

[01:08:39] Speaker B: No, no, no, I mean-

[01:08:41] Speaker C: The track?

[01:08:43] Speaker B: Yeah, like-

[01:08:44] Speaker C: We didn't do an example for that.

[01:08:45] Speaker B: 2 submissions, 3 submissions.

[01:08:47] Speaker C: I didn't make an example for that. So you mean like a list? Yeah. Submissions.

[01:08:53] Speaker B: Yeah, like- And each other. Which one, like, I saw like first one passed 1 test, second like 2 tests. Short one more. And it can be a proof for the teacher that I tried several times. Okay, I worked. Um, not very convincing.

[01:09:12] Speaker C: Okay.

[01:09:13] Speaker B: I could ask agent to work, but still it's track of work. Okay, why do I need view my code? Details. Uh, status, grade, and deadline. Status graded, deadline.

[01:09:29] Speaker C: Start repeating?

[01:09:30] Speaker B: Um, yeah, solve it in VS Code.

[01:09:33] Speaker C: Okay, so I'm gonna make it like just one part of the VS Code.

[01:09:37] Speaker B: Yeah, like solve it in VS Code and it will be- Yeah, yeah, because the description is instructions already. Okay, um, great. Then Back to assignments, all assignments. Okay. Uh. So this is submitted on November 21. I missed the deadline on November 25.

[01:10:15] Speaker C: I suggest that was just in time. We need the correct data. So it's dummy data, by the way. It's added by Python.

[01:10:24] Speaker B: Uh, I just wanted to look at how this looks, like exercise looks when I don't miss the deadline.

[01:10:34] Speaker C: This is the the bug.

[01:10:37] Speaker B: Uh-huh. The assignment is closed. Okay. Funny. Uh, ah, okay, I have to do- solve this bug. My result, uh, your fix and its grade will appear here. Fix. Okay. I think it will appear here now.

[01:11:02] Speaker C: It's appearing.

[01:11:03] Speaker B: In the details. Or is it-

[01:11:06] Speaker C: Like, go to the grade. It's here.

[01:11:08] Speaker B: Ah. Got it. It's just grayed out here. Okay. Time grayed exactly right. Okay. Uh, to do, solve this bug. Open VS Code. Okay, submit. Maybe it woke up. Uh,

[01:11:40] Speaker C: no, it's

[01:11:40] Speaker B: not condition.

[01:11:43] Speaker C: It's not condition, so we need to accept all the submission. We don't need to do some conditions like need all the tests to be correct before submission or something like that.

[01:11:54] Speaker B: Okay, then it will be usable.

[01:11:58] Speaker C: Uh, now you are going to the method one.

[01:12:01] Speaker B: Yeah, this is The main page?

[01:12:03] Speaker C: Yeah.

[01:12:04] Speaker B: Okay, does the sign-in work without this stuff? Um, but okay, for for a demo, for a usability test, it's it may even be use- useful.

[01:12:19] Speaker C: Actually, I get this idea from the requirements engineering project because the the other professor, like, getting from this role to the other role. So you are repeating, yeah,

[01:12:31] Speaker B: yeah,

[01:12:32] Speaker C: uh, adding the email and the password. So he recommend like to add this thing, it will be better.

[01:12:39] Speaker B: So yeah, I think this is a good idea.

[01:12:42] Speaker C: So just click, go back to the student.

[01:12:44] Speaker B: Yeah, I was a student, I was a professor. Okay, now-

[01:12:50] Speaker C: Because you are getting here and here at the same time, so Just need to refresh. Yeah, go to dashboard.

[01:12:58] Speaker B: Okay, so, um, okay, practice bugs, practice bugs. Oh, here is a public gallery. Kind of. Only my bugs. Um, any difficulty or languages, new bug with AI. But it's dashboard. Okay, count number of plates. Uh, okay. Oh wow. It's Dart.

[01:13:48] Speaker C: Yeah.

[01:13:48] Speaker B: Um, okay. So I can submit it, right? Can run tests. This bug has no tests. Okay. If I submit- okay, submission does not work. Uh, all practice bugs.

[01:14:13] Speaker C: By the way, the submission here, it will go to our server. Like, he will get like, graded, or maybe there is a submission from our system because there is no professor for this one.

[01:14:27] Speaker B: Uh, yes.

[01:14:29] Speaker C: Because it's a public bug.

[01:14:30] Speaker B: Yes. So one question, where am I here? Like, am I in some container on your server? Or am I on your machine?

[01:14:42] Speaker C: No, you're on the container server.

[01:14:44] Speaker B: Really?

[01:14:49] Speaker C: Try it. No, it's not connecting, so reload the window.

[01:14:59] Speaker B: Okay, I think I should- shouldn't- Shouldn't start VS Code and go back simultaneously.

[01:15:10] Speaker C: Okay.

[01:15:12] Speaker B: Uh, open VS Code. So, Code Server. Okay. Okay, this is another user.

[01:15:57] Speaker C: No, this is-

[01:15:58] Speaker B: I am on the server. Okay. Um, enter Python. Okay. Here I have another Python. Do I even have Python?

[01:16:21] Speaker C: Which Python? This is my Python.

[01:16:26] Speaker B: Yeah, okay, no Python.

[01:16:30] Speaker C: For me it's Ubuntu.

[01:16:32] Speaker B: Yeah.

[01:16:32] Speaker C: It's not the same system.

[01:16:35] Speaker B: I mean, still Linux. I just wanted to check that I have different environments. Okay, um, so yeah, we we checked that I can run code using Python.

[01:16:50] Speaker C: Submission not working.

[01:16:53] Speaker B: Yeah, um, and that I can't fix the simplest bug. And that's that's it. So-

[01:17:02] Speaker C: He can see his grade from the professor. He can create one. Try to see create a bug.

[01:17:10] Speaker B: Um, what do you mean?

[01:17:13] Speaker C: Creating a bug.

[01:17:14] Speaker B: Can I can I sign in as a professor? Ah, so I I first need to sign out.

[01:17:21] Speaker C: Sign out and go to the console.

[01:17:24] Speaker B: Um. Which case do you do you want me to try?

[01:17:30] Speaker C: Go to the dashboard.

[01:17:31] Speaker B: Okay.

[01:17:33] Speaker C: Practice bugs.

[01:17:34] Speaker B: Practice bugs.

[01:17:36] Speaker C: New one with the AI.

[01:17:38] Speaker B: New bug with the AI. Okay. I don't have an API key right now. Can set the model. I need to set the endpoint. What should the bug be about? Okay, prompt, language, easy, medium, only me, every student.

[01:17:56] Speaker C: For this one, for every student. Okay, that's what I'm going to do.

[01:18:01] Speaker B: Yeah, the AI box are not checked by Professor Shery.

[01:18:03] Speaker C: And here it's missing my VI part.

[01:18:06] Speaker B: Yeah,

[01:18:07] Speaker C: okay,

[01:18:07] Speaker B: VI can take up the meal. After I generated What do you see?

[01:18:14] Speaker C: You see the bug?

[01:18:16] Speaker B: Uh, yeah, it will not work.

[01:18:19] Speaker C: Just pick uh

[01:18:20] Speaker B: pick one of the- okay, something like this I will see. Um, so will will I see some button here like-

[01:18:29] Speaker C: Button like what? Uh, if you create a bug, it will be like coming-

[01:18:34] Speaker B: Like solve in VS Code or something like this after- Where will this bug go?

[01:18:40] Speaker C: After generation, click on selecting the bug.

[01:18:45] Speaker B: Where?

[01:18:45] Speaker C: Select the existing one. Yeah, the public.

[01:18:47] Speaker B: Here?

[01:18:47] Speaker C: Yeah.

[01:18:48] Speaker B: But I'm here at the bottom of the page.

[01:18:51] Speaker C: It will be like show you the page of the bug, the details only of the bug.

[01:18:55] Speaker B: Ah, got it.

[01:18:56] Speaker C: And if you're gonna see the code and the bug, you're going to the PS1.

[01:18:59] Speaker B: Okay. And then- I can practice, edit. Can I delete? Oh, I can delete a bug.

[01:19:12] Speaker C: Yeah.

[01:19:12] Speaker B: Great. Uh, so I edit description, language, yeah, some buggy code, expected fix. Okay, I don't see this test. Shouldn't see this. I think I should see this only in VS Code.

[01:19:32] Speaker C: But it's yours. Why you want it?

[01:19:35] Speaker B: Yeah, I mean, if I want to edit, I would not edit the back code. Then I don't want to do it here. I want to do it in VS Code because there is like my syntax highlighting, like type check. So here I should see like edit in VS Code, something like this, instead of these three fields.

[01:20:01] Speaker C: I have something like uh save the changes.

[01:20:06] Speaker B: What? Where where do you store this this code?

[01:20:11] Speaker C: It's in the database.

[01:20:14] Speaker B: So like this? Like you put these files into the file system in the container. You provide me VS Code.

[01:20:24] Speaker C: VS Code need another extension for saving changes.

[01:20:28] Speaker B: Uh, you have to test, to submit. Uh, but why?

[01:20:35] Speaker C: This is for changing, it's not like solving a bug.

[01:20:39] Speaker B: No, it will be solving as well.

[01:20:41] Speaker C: No, this is editing a bug. This screen for editing a bug.

[01:20:44] Speaker B: Yeah, but when I edit, I should check that

[01:20:48] Speaker C: This is

[01:20:48] Speaker B: correct? Yeah. I think it is a bit of abuse of the extension functionality, but I think I should be able to like run tests on my bug. Um, submit. Okay, maybe I don't need submit button. Yeah, but test button, it would be convenient.

[01:21:11] Speaker C: Okay.

[01:21:13] Speaker B: Okay, practice edit bug. Why, um, why is it edit bug, by the way? Ah, so I am a student now.

[01:21:28] Speaker C: Yeah, you're a student now.

[01:21:30] Speaker B: Yeah, why do I need to edit bug?

[01:21:33] Speaker C: This is your bug.

[01:21:35] Speaker B: This is my bug?

[01:21:36] Speaker C: Yeah, the private one. Okay,

[01:21:38] Speaker B: uh,

[01:21:41] Speaker C: Maybe the AI give you some bad and it's not so hard or something like that and you want to change it or add something.

[01:21:59] Speaker B: I'm not sure, like I have practice, yeah, here in practice I can do what you what I told you, like I can open The bug can be scored, solved, run test, submit.

[01:22:10] Speaker C: Yeah, this is the thing.

[01:22:11] Speaker B: Yeah,

[01:22:12] Speaker C: one-

[01:22:13] Speaker B: and edit my bug. It's, it's very strange.

[01:22:17] Speaker C: Like, look with me, you have the bug. Yeah, when you go to the practice, that's mean you, you will fix this bug. Okay.

[01:22:25] Speaker B: Yeah,

[01:22:25] Speaker C: but editing bug, that's mean you're editing the task itself.

[01:22:29] Speaker B: Yeah,

[01:22:30] Speaker C: so like assign another task, a topic like that, and save it.

[01:22:33] Speaker B: Okay, I can agree that I can edit those fields, but, um, but not the- yeah, I think this should just be removed.

[01:22:44] Speaker C: Okay, it was thought like for public and back. That's the purpose of adding the editing back.

[01:22:52] Speaker B: Got it. But students cannot, the teachers can.

[01:22:57] Speaker C: No. Uh,

[01:22:57] Speaker B: yeah, but they have another

[01:23:00] Speaker C: Yeah, in this meeting I guess the student can't do that.

[01:23:05] Speaker B: Mm-hm. Okay, uh then-

[01:23:08] Speaker C: So this is for the students, I think. There is another thing you're gonna add, the webcam?

[01:23:14] Speaker B: I think for the teacher, using AI to generate a bug. Yeah, but it does not work. For the student, um, mine-

[01:23:26] Speaker C: So I need to remove the editing, need removing the public one.

[01:23:29] Speaker B: Yeah.

[01:23:30] Speaker C: Like for the other students.

[01:23:32] Speaker B: Uh, only mine, only my bugs. Um, I think there should be also be some filters. Which filter? My bugs, you mean.

[01:23:45] Speaker C: My bugs mean like what the one you created.

[01:23:48] Speaker B: Yeah.

[01:23:48] Speaker C: And this one. Okay, we-

[01:23:53] Speaker B: Uh, this is- so I see the public gallery.

[01:23:57] Speaker C: Yeah.

[01:23:58] Speaker B: Um, we don't store course information for bugs, only who created them. Do we want to filter by creator or by the- rather by the by the language?

[01:24:14] Speaker C: Yeah.

[01:24:15] Speaker B: No, I think I don't need to filter by Creator.

[01:24:17] Speaker C: Yeah,

[01:24:18] Speaker B: yeah. Okay, only my box, title and description, filter. Okay, I think filtering can be uh automated. I mean, automated.

[01:24:30] Speaker C: Okay, automated.

[01:24:33] Speaker B: And then, um, okay, so you remove edit, you can move mine to some other column. What about removing debug?

[01:24:46] Speaker C: Remove the bug itself. Is it good or not?

[01:24:49] Speaker B: Continue, practice, edit.

[01:24:52] Speaker C: Because in the edit you can remove, but do you think we change edit with remove? And we just remove the bug. Uh, it's not good or not? It's good or not?

[01:25:06] Speaker B: I think that's good. No archive, just remove. But you can ask user, like, are you sure you want to remove this?

[01:25:16] Speaker C: Try it.

[01:25:21] Speaker B: Oh, great, you thought about this already. This permanently deletes one practice attempt. Yes, delete it. Okay. Great, I think I think that's it for the public gallery. Back to dashboard. And this one will work at some point.

[01:25:46] Speaker C: How we change like this uh navigator between the pages? I didn't like it because I see you are clicking here, go back, okay, go back. So it's good like uh after you have the With a sidebar?

[01:26:02] Speaker B: Mm-hmm.

[01:26:02] Speaker C: It would be easier to go between the pages.

[01:26:05] Speaker B: Yeah, or add some back button. Okay, anyway, uh, week 4 lists. Oh, okay, I'm in several groups. Who am I? Am I- I'm not Karim Benali. Who is that? Is it teacher?

[01:26:32] Speaker C: Yeah.

[01:26:33] Speaker B: Okay.

[01:26:35] Speaker C: And-

[01:26:35] Speaker B: For students.

[01:26:36] Speaker C: This group have 4 students.

[01:26:40] Speaker B: Right now I'm a student. Yeah. And I see the teacher of the group. Okay. And how many students are there?

[01:26:46] Speaker C: In my group?

[01:26:47] Speaker B: Okay. Um, not very important. For me, honestly.

[01:26:53] Speaker C: Okay.

[01:26:54] Speaker B: But, um, okay, assignment.

[01:27:00] Speaker C: This is before deadline.

[01:27:01] Speaker B: Yeah, and this is-

[01:27:03] Speaker C: This is the history.

[01:27:06] Speaker B: And past deadline, what happens to them? Like,

[01:27:09] Speaker C: it's going past deadline.

[01:27:13] Speaker B: Uh-huh.

[01:27:13] Speaker C: You can't edit it, it's removed from this one.

[01:27:15] Speaker B: Mhm. Got it. So does it go to here or like does it stay here?

[01:27:21] Speaker C: No, it's good.

[01:27:22] Speaker B: It's not pending anymore after the deadline?

[01:27:25] Speaker C: Yeah, it's just removed from there.

[01:27:27] Speaker B: Okay. Uh,

[01:27:30] Speaker C: you can go when you click in all results.

[01:27:33] Speaker B: All results, okay. Graded, grades and feedback.

[01:27:38] Speaker C: And here you're gonna see your history, not graded.

[01:27:43] Speaker B: Got it, so I can see my work and I can open VS Code and and still submit. Um. Wow. Okay. So why do I see the same two exercises here?

[01:28:06] Speaker C: What is it? It's not the same date.

[01:28:12] Speaker B: Ah, are these submissions or exercises?

[01:28:16] Speaker C: This is progress, sorry, so it's mean submission.

[01:28:19] Speaker B: Mm-hmm. So I submitted for this exercise twice. Okay. Uh, at the same time?

[01:28:28] Speaker C: No, different day.

[01:28:32] Speaker B: 15:55, 15:55.

[01:28:32] Speaker C: This one is 18:00.

[01:28:35] Speaker B: Is it dummy data?

[01:28:37] Speaker C: Dummy, everything is dummy.

[01:28:38] Speaker B: Okay.

[01:28:41] Speaker C: There's a lot of data here.

[01:28:42] Speaker B: Yeah. Okay, I got- I think that's that's it, that's what I want as a student. So I got um a dashboard. What what do I get?

[01:29:01] Speaker C: On the dashboard you can see his information.

[01:29:04] Speaker B: Yeah.

[01:29:04] Speaker C: You can see the group and the name of the professor.

[01:29:07] Speaker B: You can see grades.

[01:29:07] Speaker C: You can see his grades. He can create and practice in back.

[01:29:12] Speaker B: So if I missed deadline, I can see that I missed the deadline.

[01:29:16] Speaker C: Yes, removed from there, yeah.

[01:29:18] Speaker B: I mean, no, it shouldn't be removed. I should see that I missed the deadline. Um, you should be able to see the assignment even, yes.

[01:29:31] Speaker C: Actually, there are only the pending assignments because if he's missing deadline, that means it's not pending, it's not to-do list.

[01:29:39] Speaker B: Yeah, it's not pending.

[01:29:40] Speaker C: It's going like here.

[01:29:42] Speaker B: Uh, I think it should be in the dashboard because like, oh, it's submissions. Uh, but like which assignments I have to solve, they are here.

[01:29:56] Speaker C: Yeah, sorry, it's here in all assignments.

[01:29:59] Speaker B: All assignments.

[01:30:00] Speaker C: You're gonna see the missing one. Okay. And but here is like the most important thing is this one. That's why it's here.

[01:30:08] Speaker B: Ah,

[01:30:08] Speaker C: and if you want to see the other one, go in here. See the other one.

[01:30:13] Speaker B: Okay, there is- is there no space to show all this? Information here.

[01:30:19] Speaker C: Yeah, we have space if we just make it scroll.

[01:30:25] Speaker B: This, this can go here. This can go here. I think there's enough space.

[01:30:32] Speaker C: Change the order, okay.

[01:30:34] Speaker B: This can go here. I think you can show it just like everything here without an extra click.

[01:30:41] Speaker C: Ah, okay, okay.

[01:30:43] Speaker B: Um, recent grades. Uh, and this grades can be here maybe.

[01:30:55] Speaker C: Where?

[01:30:57] Speaker B: Um, grades.

[01:30:59] Speaker C: For what? For this one?

[01:31:04] Speaker B: This is all the grades for the assignments.

[01:31:06] Speaker C: It should be here, the grades.

[01:31:09] Speaker B: I mean, here, here is a table about assignment.

[01:31:14] Speaker C: All assignments.

[01:31:15] Speaker B: It's graded and and the grade is here.

[01:31:17] Speaker C: Yeah.

[01:31:18] Speaker B: So here it's grade.

[01:31:21] Speaker C: Only the grade.

[01:31:22] Speaker B: It's graded and the grade is here. I mean, I I think you it's enough to have one table.

[01:31:28] Speaker C: Ah, okay. It's like repeated. You feel like it's repeated. Okay.

[01:31:34] Speaker B: Mm, yeah, and here are also filters, right? Yeah, and regarding practice bugs, yeah, that's that's a separate thing. Maybe it should go here.

[01:31:48] Speaker C: No, I see it's like public. I would take all the pages or the buttons as a sidebar. That would be better for you see it and understand it.

[01:31:59] Speaker B: Okay. Uh, yeah, pending assignments. Pending will just be at the top. Like two tables, then one is pending, another one uh graded. Okay. Uh, yeah, and my box will be somewhere here. Yeah, I think that's it.

[01:32:28] Speaker C: That's enough for the student?

[01:32:30] Speaker B: Yeah.

[01:32:32] Speaker C: Okay, so we're gonna go to the admin now.

[01:32:35] Speaker B: Okay, we're going to admin.

[01:32:39] Speaker A: Admin, uh, Adel, if we continue on Russian language.

[01:32:44] Speaker C: That's okay.

[01:32:44] Speaker A: Okay. Тут чуть не последний этап. Я хочу быть в полном контексте по функционалу админа. Эта страница, на которую мы попадаем после того, как мы авторизовались на аккаунте админа. Угу. Тут у нас есть разделы учителя, студенты, администраторы, группы, задания. Также мы можем перейти туда по кнопкам раздела. Возможно, лучше их тут отобразить, как ранее сказали, или по кнопкам в карточках описания. У нас есть панельки с общим количеством заданий, учителей и групп. Короче, анбординг.

[01:33:41] Speaker B: При нажатии сюда.— Будет то же самое, что приоритет сюда?— Да.— Получается?—

[01:33:45] Speaker A: Да.—

[01:33:46] Speaker B: Ага.—

[01:33:48] Speaker A: Вот. Мы можем создавать учителей, редактировать их. Тут у нас имя, email, активный, неактивный. Возможно, лучше, как лучше удалять полностью учителей, чтоб они не отображались в списке или деактивировать их? С помощью чекбокса.

[01:34:15] Speaker B: Что значит актив?

[01:34:18] Speaker A: Ну, он может авторизоваться.

[01:34:19] Speaker B: Понятно.

[01:34:20] Speaker A: У него есть доступ.

[01:34:21] Speaker C: Он может авторизоваться.

[01:34:23] Speaker B: Угу. Наверное, обе опции стоят. Типа, вот здесь вот удалить учителя. А тут актив. Нектив аккаунт скинуть. У них же разные, типа, предназначения: удаление и активность. Удалять учителей в какой-то момент, чтобы у них там доступа не было к публичной галерее, допустим. А почему они вообще не могут вернуть? Ну да. Ну,

[01:34:58] Speaker A: это несложно.

[01:35:00] Speaker B: Рисовать. Да. Окей. Учителей не так много, поэтому ручной ввод вводится информация об учителе, паспорт. А паспорт— это который будет у учителя, типа дефолтный какой-то?

[01:35:16] Speaker A: Да.

[01:35:17] Speaker B: Угу. А его можно будет поменять?

[01:35:21] Speaker A: Ну, в теории, да.

[01:35:21] Speaker B: Ладно.

[01:35:23] Speaker A: Возможно, стоит Хмм, реализовать так, чтобы только с университетским паролем могли... Да, только университетскую почту можно было задавать или оставить это на совесть админа. То есть какую он поставит, может, некоторым учителям удобнее будет.

[01:35:44] Speaker B: Я думаю, я думаю, лучше так. Любой решает.

[01:35:48] Speaker A: Хорошо.

[01:35:50] Speaker B: Хорошо. Пароль и подтвердить пароль. Ну, наверное, я не знаю вообще, зачем, зачем подтверждение пароля нужно?

[01:36:01] Speaker A: Ну, чтобы админ был уверен в том пароле, который он задаёт. Или, возможно, создавать аккаунт и чтобы при активации аккаунта учитель или студент сам задавал себе пароль. Может,

[01:36:14] Speaker B: так лучше? Ну, так тоже можно, да. А-а. Ну, это выглядит как пересоздание пароля сейчас. Но я так понимаю, здесь админ задаёт пароль учителю какой-то дефолтный. Можно просто не скрывать пароль, типа. Вот это вот убрать. Просто, ну, админ зашёл на страницу учителя, видит, какой Какой пароль он ему задал? Вот. Может быть, даже стоит показывать текущий пароль учителям.

[01:36:54] Speaker A: Угу.

[01:36:54] Speaker B: Вот, и иметь возможность его менять. То есть это не дефолтный пароль, а это, в принципе, текущий пароль. Допустим, учитель забыл пароль, и админ посмотрел пароль и может ему скинуть.

[01:37:06] Speaker A: Хорошо, то есть выбираем второе поле, это поле. Делаем видимо.

[01:37:11] Speaker B: Да, это текущий пароль. Если он пустой, то, ну, там учитель может сам задать. Я не знаю, там есть сайнап у вас функционал регистрации? Да-да-да.

[01:37:24] Speaker A: Нету.

[01:37:26] Speaker C: Только админ.

[01:37:27] Speaker B: Тогда можно здесь какой-то не пустой пароль требовать для админа. Да. Вот. Да, админ. Да, и после этого он сохраняет учителя, если тут не пустой пароль. А-а и всё. Хорошо, создали учителя. Так, что-то... Ну, видите, инструкции можно будет чуть-чуть поменять. Ролл скинуть для участия в доспаре. Ну, это так-то очевидно, но ладно. Хорошо.

[01:38:03] Speaker A: Можем редактировать, создавать. Тут в целом то же самое.

[01:38:07] Speaker B: Студенты. Так, студенты.

[01:38:09] Speaker A: Тут у нас точно такая же форма.

[01:38:12] Speaker B: Ну, это вот может быть вообще неудобно. Потому что студентов очень много, типа 250 на курс надо добавить. Как как их добавлять по одному, что ли? Ну, я думаю, что надо какой-то CSV. Поддерживаете, вот, типа, с фиксированными названиями стопов. Что вообще, какую информацию о студенте? Ну, имя, да. По крайней мере, это другой. Email, да. Из Active. Ну, пароль ещё можно.

[01:38:48] Speaker A: Да. Не совсем понял, как добавляете студентов. Массово. То есть с помощью заготовленной таблицы, допустим, с этими атрибутами. Имя, email.

[01:39:04] Speaker B: Ну да, либо Excel-таблица, либо CSV. Да, но проблема с паролем в том, что надо как-то этот пароль студентам отправить. То есть либо он на почту им будет приходить. Либо нужен вот этот функционал для регистрации. Но там опять же как-то через почту, наверное, будет. Хмм. Далее. А, ну либо на Moodle ещё. Короче, не очень понятно, как без регистрации быть.

[01:39:49] Speaker A: Если без регистрации, то оно всё на плечи админа. И на почту уведомления. Если с регистрацией, то можно передавать, сделать функционал первого входа. То есть, когда он сам придумает себе пароль, имея уже email хотя бы.

[01:40:08] Speaker B: Угу. А-а, в общем, ну хорошо, админ должен уметь редактировать пароль студента. Я думаю, он даже... А, ну да. Если он ставит inactive, а, вернее, короче, тут делает студента inactive, студент разлогинивается. Или он только залогиниться не может?

[01:40:41] Speaker C: Inactive mean like he can't get in the website.

[01:40:44] Speaker B: Yeah, but will it sign out automatically?

[01:40:47] Speaker A: Если у него активная сессия есть?

[01:40:49] Speaker B: Да.

[01:40:50] Speaker C: Sign out from his website?

[01:40:52] Speaker B: Yeah.

[01:40:52] Speaker C: Right here. Wait a second. The scenario is the student is already in the website.

[01:40:58] Speaker B: Yes.

[01:40:59] Speaker C: And we, the admin, do inactive.

[01:41:01] Speaker B: Yes.

[01:41:03] Speaker C: The session there is supposed to be closed automatically, yeah?

[01:41:06] Speaker B: Yes.

[01:41:07] Speaker C: For us, no.

[01:41:08] Speaker B: Okay.

[01:41:09] Speaker C: We need to add that. But there is a thing, he can't do anything. Like, if he gonna change from page to page, that means it's closed. But if he like he didn't do anything, just stuck in his page, no.

[01:41:23] Speaker B: Yeah, they will see something, but they will not be able to submit anything.

[01:41:27] Speaker C: Anything. Because when he goes to "disabled", that means his token, or request, that's been going to the block.

[01:41:36] Speaker B: Right.

[01:41:37] Speaker C: That's what we did.

[01:41:37] Speaker B: So what I had in mind, for example, if we don't use email, like we don't send password to email during sign up, uh, we let the student use their just email as login. And set their password, and we trust the student. So another student may use someone else's email and set some password, and they will like log in into it. Not their- I mean, own password.

[01:42:12] Speaker C: Yeah.

[01:42:12] Speaker B: And they will log in as another student. Okay.

[01:42:16] Speaker C: But how they can log in? The student, the first, the student number Yes. Student A give all the information to Student B.

[01:42:24] Speaker B: Student B only knew the email of Student A. Student A was not signed up, okay, they did not have an account.

[01:42:33] Speaker C: Yeah.

[01:42:34] Speaker B: They they were added.

[01:42:36] Speaker C: Yeah.

[01:42:36] Speaker B: Student B knew the email of Student A. They sign up as Student A.

[01:42:45] Speaker C: But he need the password.

[01:42:47] Speaker B: They set password.

[01:42:48] Speaker C: Which password?

[01:42:50] Speaker B: Any password.

[01:42:51] Speaker C: He can't get in.

[01:42:53] Speaker B: Why?

[01:42:53] Speaker C: He needs the password of the student.

[01:42:55] Speaker B: Yeah, but like we just discussed how to deliver passwords to students.

[01:43:01] Speaker C: How to deliver passwords to students?

[01:43:03] Speaker B: Yeah.

[01:43:03] Speaker C: By email.

[01:43:05] Speaker B: Okay.

[01:43:06] Speaker C: We send them to his email, like what I did to the email of the university. This is your email and this is your password.

[01:43:15] Speaker B: Okay, so it's doable, like deliver uh passwords.

[01:43:23] Speaker C: Or you want to make it as OTP?

[01:43:25] Speaker B: No, no,

[01:43:26] Speaker C: uh, it's really cost a lot.

[01:43:28] Speaker B: Uh, yeah, I mean, yeah, if, if email is okay, like if it works, then great, you just send to the email

[01:43:38] Speaker C: Yeah.

[01:43:38] Speaker B: Okay.

[01:43:41] Speaker C: Or you wanna ask- give him an option for changing the password? I don't think that's needed. It's good, but it's not needed.

[01:43:52] Speaker B: Yeah, like, for simplicity, yeah. Maybe like on each change of password here, you just send, send it to email. Like, if admin changes the password, New password is sent to the student email. Then student will always know their password.

[01:44:12] Speaker C: Yeah.

[01:44:13] Speaker B: Okay. Set by admin. Okay.

[01:44:18] Speaker A: Также кнопку удалить, наверное, сюда.

[01:44:20] Speaker B: Да. Ну да.

[01:44:25] Speaker A: Так, ну у админа то же самое. Наверное, сделаем, чтобы нельзя было самого себя удалить. А с другим админом?

[01:44:36] Speaker C: Другой админ.

[01:44:36] Speaker A: Всё то же самое.

[01:44:37] Speaker B: Угу.

[01:44:38] Speaker C: Мекетак.

[01:44:41] Speaker B: Э-э-э и другой админ не может меня удалить тоже, да? Потому что я его добавил? Или...

[01:44:49] Speaker A: Такое не предполагалось. Ну, если нужно, можем сделать.

[01:44:53] Speaker B: Эм. Ну, не знаю, наверное, нужно, да. Вернее, нет. Наверное, не нужно. Админы же знают друг друга, они доверяют друг другу, так что да. Если админ перестал работать над этим проектом, можно его удалить просто и всё. Окей.

[01:45:19] Speaker A: Тут строка поиска везде.

[01:45:20] Speaker B: Угу.

[01:45:22] Speaker A: Группы. Можно создавать группу, можно редактировать. Name, description и ответственный учитель. Что-то ещё нужно для группы?

[01:45:36] Speaker B: Так, название, описание, ответственный учитель. Ну, серч по учителю, чтобы его быстрее найти. И ещё Ну, мы обсуждали, что можно в описание курса писать. Может быть, тут какой-то плейсхолдер текст, типа название курса, что-нибудь такое. Да. Ну, типа, можно, да, новое поле, new field or just instruction for admin, like write the course. Yeah, I think some validation is like prevent a separate field would be better.

[01:46:31] Speaker C: Yeah.

[01:46:31] Speaker B: Okay, uh, это было create a group. Okay, я не видел, что там. Там просто не подчеркивается. Да. Так. Ещё раз, я могу управлять

[01:46:54] Speaker A: участниками.

[01:46:55] Speaker B: А, ну это вот ты создавал группу?

[01:46:57] Speaker A: Да.

[01:46:58] Speaker B: Так, окей. Edit group, assign teacher. Ну да, один teacher на группу. Хорошо. Manage members.

[01:47:10] Speaker A: Это меня не туда ведёт. Сразу в корень.

[01:47:16] Speaker B: Ну, тут желательно какой-то поиск по студентам. Да. Ну, это единичного студента добавить.

[01:47:29] Speaker C: Потому что все студенты здесь одинаковые.

[01:47:32] Speaker B: Ну я-я I think admin doesn't want to add one student at a time.

[01:47:37] Speaker A: Checkbox maybe.

[01:47:39] Speaker C: Ah, so it's going here. It's better. Like he like he assigned the student to his group from the student page, not from the group page. You recommend that? Like from here he can he add the

[01:48:01] Speaker A: Нет.

[01:48:01] Speaker B: Здесь он может добавить студента просто без группы. Ну, тут нету группы, типа. Проблема в чём? Если 30 студентов надо добавить, как их добавить? Наверное, тоже можно.

[01:48:20] Speaker A: Тут будет список студентов и возможность поиска и возможность выбирать список. Ну, то есть чекбоксы. По кнопке добавлять массово их.

[01:48:29] Speaker C: Test it. Remove those.

[01:48:31] Speaker B: What? How?

[01:48:32] Speaker C: Those students. Remove it.

[01:48:34] Speaker B: Remove. Okay. Remove, remove.

[01:48:39] Speaker C: Uh-huh. Add. Try to add there.

[01:48:44] Speaker B: Add here? What?

[01:48:46] Speaker C: There, there. On the selection.

[01:48:49] Speaker B: Don't get it.

[01:48:51] Speaker C: Refresh the screen.

[01:48:53] Speaker B: Okay.

[01:48:54] Speaker C: Go here to add the students. Yeah.

[01:48:57] Speaker B: Okay. And add it. Why couldn't I see that student? Um,

[01:49:07] Speaker C: you added to the group, yeah.

[01:49:09] Speaker B: Ah, because I already added it to the group. Okay. Removing a student keeps the group, its assignments, Existing submission history unchanged. Yeah, I agree.

[01:49:26] Speaker A: Ты говорил по поводу того, чтобы добавлять студентов в группу прямо вот отсюда. Возможно, стоит добавить кнопку какую-нибудь добавления в группу.

[01:49:37] Speaker B: Угу. Как вообще кому для этого делать?

[01:49:55] Speaker C: It's from the student, I think, because it's easier. Because when you go to the group section and you have a list of students, you can't miss clicking for each one at all. But if you are here, you are sure for this student. This is visible. Because you're gonna only select one or two maximum.

[01:50:21] Speaker B: Да. Ну, короче, проблема в том, что я для каждого студента это должен делать. Может быть, стоит поддерживать загрузку таблички. А что там ещё? А и пароль. Ну да, короче, табличка такая может быть. Там имя студента, email, статус, что ещё? Пароль, группы, несколько групп. Вот. И-актив. Да, актив уже посчитали. Я, да, и всё. И это должно быть идемпотентно, типа загрузил табличку с теми же данными, они, ну, короче, применились. Там студент один раз добавился. А как я эту табличку сделаю— это уже моя проблема. Так. Ну, наверное, да. Наверное, моя проблема. Хмм.

[01:51:44] Speaker A: Ну и тут где-то кнопку импорта сделать, чтобы массово.

[01:51:47] Speaker B: Да. Ну, ещё аварик есть. Вариант. Здесь чек-боксы какие-то. И контекстное меню, типа добавить в группу или убрать из группы. Или сделать активным, инактивным. Ну, или здесь вот просто действия какие-то. Вот. И тогда будет удобно добавлять в группу. Нужна ли будет тогда таблица? Ну, допустим, мы вообще всех студентов добавили с первого курса 250 человек. Вот, допустим, мы всех выделили, ну, не все активные по умолчанию. Что нам может быть интересно? Ну, добавить их в группу, интересно было бы.

[01:52:46] Speaker A: Да, в уже существующую.

[01:52:47] Speaker B: Да. Но чтобы добавить в группу, нужно выбрать из этих 250 30 студентов. Это не очень удобно. Ну, возможно, у меня есть какой-то файл с модуля экспортирования, где там студенту группа его записана. Ну, или как-то каким-то образом я В общем, сделал такой файл. Тогда я бы его загрузил. Где бы я его загрузил? Здесь или здесь, в группах? Я бы, наверное, здесь загрузил. Потому что тут название группы и студенты. И всё, да? Имя и студенты. Короче, я бы сделал всё-таки загрузку файла вот здесь вот в группах. В таблице типа название группы, профессор, ну, количество студентов не надо. Эм. И-информация по студентам. Да.

[01:53:56] Speaker A: И они будут создаваться при загрузке этой таблицы.

[01:54:00] Speaker C: Это CSV-файлы, что ли?

[01:54:03] Speaker A: Нет, CSV.

[01:54:04] Speaker B: Да. Наверное, по одному. По одному ряду на каждого студента. Хмм, потому что какие ещё варианты? Да.

[01:54:17] Speaker A: То есть при загрузке файла, если там есть студенты, которых нету в сервисе, они создаются?

[01:54:23] Speaker B: Да.

[01:54:23] Speaker A: Хорошо. Если есть, то они создаются.

[01:54:26] Speaker B: Да. А, ну и ещё поле с паролем, наверное, стоит сюда же добавить. Хм. Да. И всё, это будут группы. Или если... А, ну если... Ну, поле с паролем необязательно, типа, если только дефолтный пароль для студентов создаём. Если у них sign up будет, то они сами создадут себе.

[01:54:57] Speaker A: Или уже, как ранее обсудили, на почту отправлять? Да.

[01:55:00] Speaker B: Да. Так, окей, assignment stays teacher workflow.

[01:55:06] Speaker A: Тут только просмотр информации о задании. Вообще, честно говоря, не понимаю, с чем это надо отбить.

[01:55:15] Speaker B: Redonly administrative context. Ну, разве что удалить из публичной галереи принудительно. Какое-то задание. Не знаю, тут я бы на профессора полагался. Блин. Ну, только если у профессора доступа нету к публичной галерее. Так, ну это ассаймент, это не просто Экзерсайзы. Что-то сложно. Еще раз, что мы можем сделать? Мы можем просто посмотреть. Find the bug and submit your fix. Хм. И зачем нам это нужно? Я не знаю. Я думаю, что это не нужно, да. Если нам захочется, мы просто смотрим, какой пароль у профессора, и логинимся в его аккаунт и потом управляем всеми аксессайзами и ассайментами. Вот. А так, по-моему, не нужно. Да. Ну вот группы нужны. Э-э-э. Тогда что? Тогда загрузка студентов будет через группы, наверное, проходить.

[01:56:54] Speaker A: Ну, не полная. Можно также единично создать.

[01:56:58] Speaker B: А, ну да, да. Да, до типа студенты не привязаны к группе пока что. Загружены, но не привязаны, такое может быть.

[01:57:08] Speaker A: Бывает же допнапор на всякий. Какие направления? И когда это происходит, то у профессора нету отдельной таблицы, есть кто допоступил. Наверное, есть. Ну, в любом случае. Ладно.

[01:57:28] Speaker B: Хорошо, а здесь, блин, не знаю, может В одном месте сделать вот эту загрузку таблицы. То есть, допустим, если группа и профессор не указаны, то тогда вот сюда добавятся студенты. Зачем нам вообще нужны группы и студенты?

[01:58:02] Speaker A: Ну, как минимум, студенты нужны для того, чтобы удалить. То есть через группы мы это не можем сделать. Удалить студента какого-то.

[01:58:13] Speaker B: Мы можем добавить в группу. Угу. Короче, через группы мы можем. А, или это мы из группы?

[01:58:25] Speaker A: Из группы.

[01:58:26] Speaker B: А, совсем удалить не можем?

[01:58:27] Speaker A: Да. Ну и отредактировать всю информацию по нему.

[01:58:33] Speaker B: Не знаю, мне кажется, тут можно одну табличку сделать, типа, там имя студента, email, группа, а-а, что ещё там, профессор и

[01:58:48] Speaker C: всё.

[01:58:48] Speaker B: И всё.

[01:58:49] Speaker A: Групп же несколько может быть.

[01:58:51] Speaker B: Вот. Да. Теперь Э-э, добавляем фильтр по группе, чтобы выяснить, ну, чтобы работать со студентами одной группы. Это у нас получается типа как manage members. Э-э, при, ну, после применения этого фильтра можно выделить несколько студентов, убрать их из группы. Э-э, если нужно добавить студентов, ну, мы их просто ищем по email или там по группе. Опять же, под другое. Теперь что ещё? Ну, учителя поменять мы не можем или можем? Учитель как-то к группе привязан же?

[01:59:32] Speaker A: Да. Ну, тоже можно реализовать какую-нибудь кнопку замены учителя после того, как выберем.— Группу?—

[01:59:45] Speaker B: Угу.— Либо в группах чисто группа и учитель маппинг будет без управления пользователями. Да, в студентах уже, ну, в студентах больше всего. Вот. И при выборе группы профессор автоматически будет указываться. Так. Что ещё тут нужно? Edit группу, сайт teacher. Ну да, это всё вот здесь можно, в принципе, сюда вынести. Actions с группой студентами по группе будет здесь происходить. Так. Теперь Ну всё, вроде мы распределили функционал.

[02:00:44] Speaker A: Угу.

[02:00:45] Speaker B: Или ещё какой-то комментарий был? Нельзя делать со студентами.

[02:00:50] Speaker A: Это удаляем. Создание группы оставляем здесь. Тут оставляем группу, учителя. Количество студентов можно оставить на всякий случай. Ну, не—

[02:01:01] Speaker B: Мешает?— Ну да.— Ну, управление студентами, как будто удобнее было бы прямо отсюда из студентов. Ну, либо как-то надо...—

[02:01:12] Speaker A: А тут мы оставляем, получается, только смену учителя?—

[02:01:17] Speaker B: Мы её вообще даже тут можем сделать, типа дропдаун-лист какой-нибудь.—

[02:01:21] Speaker A: В студентах, да?—

[02:01:22] Speaker B: Не, в группах.—

[02:01:24] Speaker A: Ага.—

[02:01:24] Speaker B: Угу.—

[02:01:26] Speaker A: Да.

[02:01:28] Speaker B: Ну, не знаю, ситуация, что у нас сто учителей, мы не можем найти нужного.

[02:01:35] Speaker A: Ну, там строка поиска.

[02:01:38] Speaker B: Да-да, какая-то. Хорошо. Добавление студента— это там будет?

[02:01:42] Speaker A: Угу.

[02:01:45] Speaker B: Edit Group. Название группы можно прямо там отредактировать.

[02:01:50] Speaker A: Да.

[02:01:51] Speaker B: Описание. А

[02:01:54] Speaker A: учителя можно вот В этой же форме менять.

[02:01:59] Speaker B: Здесь?

[02:01:59] Speaker A: Вот тут будет кнопка edit.

[02:02:02] Speaker B: А, ну да.

[02:02:03] Speaker A: И там поле выбора учителя останется.

[02:02:06] Speaker B: Можно.

[02:02:07] Speaker A: Участники группы не будем отображать их. Ну, то есть количество будем, а хотя зачем количество отображать, если мы не будем отображать список?

[02:02:16] Speaker B: Не особо нужно.

[02:02:18] Speaker A: Окей.

[02:02:20] Speaker B: Здесь можно его получить. Профиль струвов по группе.

[02:02:24] Speaker A: Угу, каунтер будет.

[02:02:25] Speaker B: Да.

[02:02:26] Speaker A: Хорошо.

[02:02:28] Speaker B: Так, и всё.

[02:02:32] Speaker A: То есть вот.

[02:02:34] Speaker B: Ну да, удаление студентов там же будет в студентах.

[02:02:39] Speaker A: Грубо говоря, вот по нажатию этой кнопки мы сразу вот сюда переходим. Тут мы можем выбрать учителя. Описание, поменять имя. Всё. Это удаляем. Остаётся три колонки. Хорошо.

[02:02:59] Speaker B: Вопрос: а зачем? Зачем edit? Можно же, в принципе, здесь просто поле добавить, типа description, типа, не знаю, там по-двойному. Ну, здесь вот выбор профессора через там выпадающий список, допустим. Здесь название группы.

[02:03:28] Speaker A: Да, мы можем брать любую кнопку и просто кликабельным сделать поле, переходить в него и редактировать. Понял.

[02:03:38] Speaker B: На самом деле, может быть, не выпадающий список, потому что мы не знаем, какие профессора есть. Какие группы есть? Эм. Ну, типа, я не знаю, просто это исчерпывает всю информацию или нет. Если бы у нас был отдельный список профессоров, которые могут быть, и отдельный список групп, то можно было бы везде выпадающий список сделать. Вот если Ну, профессора могут не указываться сначала.

[02:04:16] Speaker A: Ну, выпадающий список учителей у нас уже в том поле есть. Вот тут.

[02:04:21] Speaker B: Вот откуда, откуда мы знаем, какие учителя? Где мы взяли? Где мы сохранили? А-а, ой, господи. Да, у нас есть учителя в группах у нас. Да, в группах у нас уже известны учителя. То есть мы тут просто группу... Угу. Хорошо. Ну и описание группы тогда. И всё тогда, не нужны вот эти кнопки, по-моему.

[02:04:54] Speaker A: Описание прямо в этой строке или по нажатию проваливаемся туда и видим?

[02:04:59] Speaker B: Там даже точнее, наверное, ку... Курс или как-то. Хмм. Сейчас. Ну да. Туда описание прямо взять. Я не знаю, какой-то лимитный символ можно поставить и сказать, что это вообще курс.

[02:05:26] Speaker A: Описание курса.

[02:05:28] Speaker B: Да. Блин, я не знаю, просто нельзя провалидировать название курса, потому что нету вроде как стандарта. Точнее, нет, название курса есть. Давай просто название курса тогда. Вот. И всё. И полагаемся на админу, что он правильно введёт. Например, МСД ведёт. Вот.

[02:05:57] Speaker A: То есть при создании группы мы указываем название курса ещё? Да. То есть тут дополнительное поле будет при создании группы. Хорошо.

[02:06:09] Speaker B: Угу. Ну да, это мы же обсуждали, типа, где-то курс, ну, Адель предложил поле новое сделать, да? Описание... Описание, я не знаю вообще, нужно или нет. Описание чего? Курса, группы? Не, я думаю, не нужно. Просто название и курс, типа МСД, там группа один. Ну, ну не МСД, конечно, там другие курсы, где программируют. Да, всё, это заполнили группы. Теперь можем воспользоваться группами. Здесь в студентах администраторс. Не знаю, может, их перепорядочить, типа, что выше, что нижнее. Да пофиг, ладно, не надо. Администраторс здесь. Угу. Паспорт, конферм паспорт. Да. Ну, конечно, это можно было бы сюда в таблицу. Вынести. Всё. Ну ладно, так удобнее. По-моему, у меня больше нет комментов. Есть какие-то вопросы по студентам?

[02:07:29] Speaker A: Да нет, всё чётенько.

[02:07:32] Speaker B: Отлично. Да.

[02:07:38] Speaker A: Да, всё.
