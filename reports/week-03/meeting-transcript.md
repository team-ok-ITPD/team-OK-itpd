# Prototype validation meeting transcript

- **Date:** 16.10.2026
- **Participants:** <names> (Speaker A, Speaker B, Speaker C)

**[00:00:00] Speaker A:** Uh, as we understand the project, it will be wonderful
for creating challenge. Okay, so is that good art design?

**[00:00:16] Speaker B:** I have no idea.

**[00:00:18] Speaker A:** Like choosing the language here, the— you know, like
you can start from this. This is the history of the—

**[00:00:28] Speaker B:** So how do I know that How do I know how to choose a
language?

**[00:00:34] Speaker A:** With this button, this button here.

**[00:00:36] Speaker B:** Is it very intuitive? Um, ah, so I'm not sure. Maybe
there should be like main [inaudible] somewhere here in the center.

**[00:00:47] Speaker A:** Okay, okay. So take the language to here because,
because in the requirements we mentioned, uh, the first language for Python and
second and third version, it will be like more languages.

**[00:01:00] Speaker B:** Uh, sure, but this one is a prototype, right?

**[00:01:04] Speaker A:** Yeah, yeah, that's a big one [inaudible].

**[00:01:08] Speaker B:** The goal for prototype is to show how the product will
feel, how it will look like. I'm sure this design may be used later, so it's not
about—

**[00:01:22] Speaker A:** Do you want to like the code itself. Like, you kind of
want to click the page and see the buttons on the board.

**[00:01:28] Speaker B:** No, I don't want it. I want to discuss how the
interface may be structured to provide better user experience. This is why I'm
asking why this button is so small and it's here.

**[00:01:45] Speaker A:** Okay, so we need to change this one?

**[00:01:47] Speaker B:** Yeah, I mean, for me it's not immediately
discoverable. But yeah, okay.

**[00:01:56] Speaker A:** For the the challenge itself, there is two types: with
AI generating, and the other one is like from the history.

**[00:02:05] Speaker B:** So what do I see when I enter the site?

**[00:02:09] Speaker A:** When you enter the site the first time?

**[00:02:11] Speaker B:** Yeah. You see the screen?

**[00:02:13] Speaker A:** No, you create the login basic screen. It's nothing.

**[00:02:16] Speaker B:** Okay, after the login.

**[00:02:18] Speaker A:** This one with the null history. You don't have history
here.

**[00:02:22] Speaker B:** Okay, you don't have anything. You just have the— it's
like a form.

**[00:02:22] Speaker B:** Okay,

**[00:02:28] Speaker A:** you just here fill your data. Here you can type to the
AI, and after that you submit or start the challenge.

**[00:02:38] Speaker B:** Okay.

**[00:02:39] Speaker A:** When we do this, the challenge go to the AI or to our
backend. And after that, after generating the challenge itself, it goes to the
second page. It's the practice page.

**[00:02:51] Speaker B:** Okay.

**[00:02:52] Speaker A:** Here we're gonna practice. Here, write the code and
test it. This is the test.

**[00:02:58] Speaker B:** Okay. So how do I run the debugger?

**[00:03:05] Speaker A:** The result of the debug?

**[00:03:07] Speaker B:** No, like real debugging tool. Set the breakpoint, run
code to that breakpoint.

**[00:03:15] Speaker A:** Aha, you wanna like real, real debug it, like set the
breakpoint?

**[00:03:22] Speaker B:** Yeah, like I need to debug the program. So you want to
debug [inaudible]

**[00:03:26] Speaker A:** In my, in my thing, uh, or as I understand the first
time, it's like Leetcode. You write the code, you go there, so if the code have
error It will show the error here as a remark, the result of the debugger, or
maybe the result of the console. And this is the test. If your code is
syntactically and everything is good, but there is semantically error, so it
will be showing the result. This one is correct, this one is not, and so on.
Okay. But about the features of... How can say... the the blocker of the code
and so on, which is used in the VS Code as a website? No, it's not in the
website. You have the SSH. We can provide an SSH later. Like he can take it and
put it in the VS Code and directly work from the VS Code.

**[00:04:22] Speaker B:** How does he submit the solution from VS Code?

**[00:04:27] Speaker A:** Take it from VS Code and paste it here.

**[00:04:29] Speaker B:** Paste it here. Okay...

**[00:04:30] Speaker A:** yeah, it's not a good idea?

**[00:04:34] Speaker B:** The catch is that we would like to support
multi-module exercises like in real development.

**[00:04:42] Speaker A:** So you want like an idea to make him submit from VS
Code directly?

**[00:04:47] Speaker B:** Ideally, yes, yes. And VS Code may be a standalone
application or somewhere in the browser, but I'm not sure... how to work with
[inaudible].

**[00:04:58] Speaker A:** I think for this, I think for this thing we need like,
uh, the good thing is create an extension to VS Code.

**[00:05:05] Speaker B:** Yeah, might be an approach.

**[00:05:07] Speaker A:** Should be good.

**[00:05:11] Speaker B:** Yeah, I mean, the need is to conveniently debug
programs, and VS Code is very much suited for this.

**[00:05:23] Speaker A:** Yeah, VS Code is the good one.

**[00:05:25] Speaker B:** And so this shouldn't be like a single editor.

**[00:05:30] Speaker A:** Yeah, you mentioned before, uh, the good thing is like
using, uh, VS Code online editor.

**[00:05:37] Speaker B:** Yeah, that might be an option too. Um, I mean, can be
a standalone or can be online, you can decide it a bit later. We can discuss
other parts. So somewhere there will be like progress.

**[00:05:54] Speaker A:** This is the test, not the progress. Like the test and
the result of the code.

**[00:06:00] Speaker B:** What is a test? Like —

**[00:06:02] Speaker A:** A test, like, uh, let's take an example. Uh, if you're
gonna— how we can say— let's take an example for the code. Let's set the primary
code or something like that, a primary number or something like that. So, uh,
the, the our AI have the result. So you have the input and the output
expectation. So if your code or your writing code didn't get our expectation or
didn't get the real result or output, that means you are wrong.

**[00:06:39] Speaker B:** Uh, I mean, you have several tests like 1, 2, 3, and
you run them, and here you got the expected results and here you didn't.

**[00:06:50] Speaker A:** This is the expected result. Like —

**[00:06:52] Speaker B:** where are they? Like, runs in the code. Like first
time you run all tests, second time you run all tests.

**[00:07:01] Speaker A:** The test is— all the tests are [inaudible].

**[00:07:05] Speaker B:** Okay,

**[00:07:06] Speaker A:** wait, here, like, expected number is 5, but the actual
number he can— we get it from this code is 0. So that's, that means it's wrong.

**[00:07:15] Speaker B:** Okay, so I assume those are 3 separate unit tests, and
they run with this function. And the first test expected 0, got 0. Second test
expected 5, got 0.

**[00:07:30] Speaker A:** Yeah,

**[00:07:31] Speaker B:** okay,

**[00:07:32] Speaker A:** so that means there is a logic error in the code.

**[00:07:35] Speaker B:** Yeah, right. So there can be multiple tests. That's,
that's a good approach.

**[00:07:42] Speaker A:** But we need to make limits for the tests number. Like,
I took the idea from LeetCode. LeetCode generally give only 3 tests and you can
edit the test as you like.

**[00:07:56] Speaker B:** Yes.

**[00:07:56] Speaker A:** For the numbers, the output and the input. The
LeetCode is working like that. So that's why I take— put this 3 and

**[00:08:10] Speaker B:** On Codeforces, you see all tests unless it's a
contest. And to, to edit the test means like to create a file with the right
input. So you edit tests locally in a file. So, um, these tests, how are they
stored? Here. Actually, what is stored there?

**[00:08:40] Speaker A:** Uh, in the environment. In the environment, you mean
on the backend of the server?

**[00:08:45] Speaker B:** Yeah, there are files like the test files.

**[00:08:48] Speaker A:** Those are the files, right? JSON files. Input, output,
input, output.

**[00:08:55] Speaker B:** Okay, they are created from AI.

**[00:08:59] Speaker A:** Yes, as he depended on it.

**[00:09:01] Speaker B:** I'm going to say it by humans, probably.

**[00:09:04] Speaker A:** Yeah, but it's by Python script. Because like the AI
give the problem and all at the same time solve the problem.

**[00:09:17] Speaker B:** Yes.

**[00:09:17] Speaker A:** And he give the inputs using his code, getting the
outputs and giving us the JSON files as a result. So the JSON file, we have
input output. How we can validate or verify this Is good or not is from the
Python script. Python script what you see, see the result from this one.

**[00:09:39] Speaker B:** Okay.

**[00:09:40] Speaker A:** And compare the input, the output from the testing and
what we have already in JSON file from the AI.

**[00:09:47] Speaker B:** This way you check conformance of yeah the test code
with the test code yeah to the test yeah. Like if expected values like if
received values — I don't know, I don't check. Um...

**[00:10:07] Speaker A:** it's like we're taking the input from the JSON file,
running there, and comparing this result with the, the other results from the
JSON we are taking the input from it.

**[00:10:18] Speaker B:** So the JSON is produced by AI?

**[00:10:22] Speaker A:** Yeah.

**[00:10:22] Speaker B:** Yes, and it expects that the program fails, and if it
doesn't fail, then the code is wrong. Because it should fail, because AI expects
that it fails. So what is the source of truth? Like code or test?

**[00:10:38] Speaker A:** The truth?

**[00:10:39] Speaker B:** Yeah.

**[00:10:39] Speaker A:** It's the test. It's like code is correct or not.

**[00:10:44] Speaker B:** Yeah, does it like— does it fail as we expect it to
fail? I want it to fail somewhere. Like I say—

**[00:10:53] Speaker A:** Usually yes.

**[00:10:54] Speaker B:** Like I want this bug. How do I ensure that AI produced
exactly this bug?

**[00:11:03] Speaker A:** We're given the problem to the AI and the AI give us—
the AI already give us the bug.

**[00:11:09] Speaker B:** Yes.

**[00:11:10] Speaker A:** And the solution of the bug.

**[00:11:12] Speaker B:** Yes.

**[00:11:13] Speaker A:** Yeah. So we have 2 things to— we can do it. One of
them is testing the, like, comparing the code which AI given this one. And this
is not really good idea because the code you can't Compare the code.

**[00:11:28] Speaker B:** Why?

**[00:11:29] Speaker A:** I don't know how to compare in two codes. Like here we
have different values, different variables, different so on. You see?

**[00:11:36] Speaker B:** Come on, you have diff. So you may ask AI to produce
like an oracle right solution. Then from this oracle, yeah —

**[00:11:46] Speaker A:** The solution itself can be different from one problem.
Maybe some student using recursive function, but the other one using 2, 4,
including themselves, and both of them are solutions, both of them are correct,
given the good result. So what we compare, we compare only the input and the
output.

**[00:12:12] Speaker B:** That's right. Like, uh... no, I mean, for me as an
exercise author, I should be able to see where the bug is and how it looks like.

**[00:12:28] Speaker A:** Yeah, yeah, yeah.

**[00:12:29] Speaker B:** So if I ask an AI, please generate me exercise, I
think it should generate like 3 files. The first file is the correct program,
the second file is a buggy program, and the third file is tests that reproduce
the bug in the buggy program.

**[00:12:49] Speaker A:** About the test, how would it look like? For me it's
JSON files.

**[00:12:54] Speaker B:** Tests may be a Python file, like testing for Python
tests. Yeah, and then this test must pass on the correct program and must
reproduce the bug on the buggy program.

**[00:13:13] Speaker A:** Okay. The part of pytest, I didn't like actually think
about that, to be honest. I thought just taking the write code, the debugging
code, and the input/output JSON. So yeah, it's, it's a good idea to write in
pytest.

**[00:13:34] Speaker B:** Yeah, might be a good idea, like, uh, in Python If
they edit the program in some nasty way, then in Python you can handle some
exceptions. If you use just a JSON and somehow compare the codes, you may not
know, like, whether the— you may receive some behavior that you don't handle,
and then, like, the whole server can crash. But if you—

**[00:14:05] Speaker A:** Can you give an example, like, from behaviors I can't
handle?

**[00:14:10] Speaker B:** For example, they rm -rf /var directory. You can parse
the program and see that this command is executed, but for this you need to
write like Python, like real Python code. But if you use just JSON, you can't
see that they do some bad things.

**[00:14:37] Speaker A:** I get that.

**[00:14:38] Speaker B:** Something like this. So either you need some generic
setup, generic harness that will like check that the program that they submit
doesn't do anything bad, or you could run their program on their device, on
their computer, so that if the program does something nasty something bad, then
it harms their computer.

**[00:15:06] Speaker A:** Um, so we need to run the program in his computer, and
that's why this might

**[00:15:11] Speaker B:** be an option. Yeah, or you run your computer on server
but somehow sandbox it so that it doesn't do anything bad to other— like

**[00:15:24] Speaker A:** maybe a container.

**[00:15:24] Speaker B:** Maybe a container.

**[00:15:27] Speaker A:** Container, just run the code there and seeing the code
how it will be like behaving with the VM. But if you will like, it will like
take a lot of time. It's like, uh, like at the performance.

**[00:15:43] Speaker B:** I don't know why. Maybe like you spin a container and
then you can run the program several times, just replace the file like as it
said to do.

**[00:15:55] Speaker A:** Mhm, yeah, that's possible. So yeah, generally, uh, as
I understand, so I need like to add another thing here. You said the console to
see the error, to show me the error exactly where is it.

**[00:15:55] Speaker B:** Yeah.

**[00:16:12] Speaker A:** uh, about the red dot, that's not possible.

**[00:16:15] Speaker B:** Not where the error is, but like just output of the
tests. Like I want to see what the tests output. It may be Like this, like very
compact value, maybe 0. Yeah, this might be like 1,000 values. I mean, this
interface, like where there's one row, may not be optimal.

**[00:16:34] Speaker A:** Okay, okay. So it will be best if we, uh, add the
console, the console here to see the result of the Python, how it will interact.

**[00:16:44] Speaker B:** It's possible to see full output of the test.

**[00:16:46] Speaker A:** Yeah, we need to see the full output of the test. So
yeah, I think that's it for creating. There is a remark here, you mentioned the
language, it will be here in the middle of the form. It will be better.

**[00:17:04] Speaker B:** Okay, what's this exercise preview? So it was
generated.

**[00:17:11] Speaker A:** Yeah, it gives you the, like, the preview. Okay, and
so on. And you Started or consulted.

**[00:17:17] Speaker B:** Yeah, as we discussed, there can be multiple files, so
maybe it doesn't always make sense to review the code itself and tests. Um,
so...

**[00:17:31] Speaker A:** So we remove this side to be better?

**[00:17:36] Speaker B:** I don't know, maybe it should be something.

**[00:17:38] Speaker A:** Why I like showing this one? Because if we chat with
our AI, there is no always given us what I expected. Sometimes they give me like
something easy, maybe something I already did it before, maybe something you
see. So that's why I show him the code. That's not the right code. So so yeah,
and dimension the wrong. It's like the description of the challenge. And after
that, when you press start, you go there. If he didn't press that icon, so he go
to fill the form again.

**[00:18:22] Speaker B:** Yes—

**[00:18:23] Speaker A:** But I know it's 3 files, but we're showing only 1
file.

**[00:18:31] Speaker B:** This works for very simple problems. Like where you
can see the whole result in a like little—

**[00:18:38] Speaker A:** So if it was big, it will be like problem.

**[00:18:40] Speaker B:** Yeah, if it's like 1,000 lines file, then what do you
preview and why do you preview it here in a little window? If I— if you can like
directly go to the exercise, see if it's—

**[00:18:53] Speaker A:** Okay, that's good, that's good.

**[00:18:56] Speaker B:** Yeah, here like this, um, This, what is shown here for
the code?

**[00:19:05] Speaker A:** Description, this function.

**[00:19:07] Speaker A:** So this is like description, the requirements about
like the logic of the program, maybe, and description of the bug.

**[00:19:15] Speaker A:** Yeah, it's answer. All of that is answer from the AI.

**[00:19:19] Speaker B:** Yes.

**[00:19:20] Speaker A:** So we just formulated like that.

**[00:19:22] Speaker B:** So some hints about what can go wrong in the program,
like so that You know where to look at.

**[00:19:29] Speaker A:** Yeah.

**[00:19:29] Speaker B:** All right, so this is okay.

**[00:19:31] Speaker A:** So look in the input, how— with the input, how— what
we need, what we expected, but the actual result is this from this code. So we
need to fix this code to get the expected thing.

**[00:19:43] Speaker B:** So, um, this is— this will be good as a tutorial for
the interface, like how you will see The output, how you will see the program.

**[00:19:57] Speaker A:** But yeah, it's not reliable for the big program, it's
just for small programs.

**[00:20:03] Speaker B:** Yeah, but yeah, and probably it will look different in
VS Code because, um, okay, this might look the same way in VS Code in the
terminal. But like here it looks like outside of VS Code doesn't like really
give you a lot of information. So...

**[00:20:28] Speaker A:** so I think we need to remove the code.

**[00:20:31] Speaker B:** Yeah.

**[00:20:32] Speaker A:** and just put the description of the code.

**[00:20:36] Speaker B:** Yes.

**[00:20:37] Speaker A:** like from the big project to the description line.

**[00:20:40] Speaker B:** Like, uh, yeah, here, here I think should be like a
preview of a prompt that AI uses to generate an exercise. So you give it a
topic, you give it a bug, and it comes up with like a plan of where it will like
put a bug, but like very generic, like vague plan so that it doesn't give you
all details. Then you can—

**[00:21:07] Speaker A:** So we can name it like a description for the debug,
but the output We need to remove it or not?

**[00:21:13] Speaker B:** Yeah, also it's not needed.

**[00:21:16] Speaker A:** Okay, so remove those 2.

**[00:21:18] Speaker B:** This will be just like description of the problem,
problem statement. Okay, um...

**[00:21:25] Speaker A:** and this will be bigger.

**[00:21:26] Speaker B:** Yeah, and I know on LeetCode and Codeforces they show
like examples of input and output, but you can show it in VS Code. Yeah, you
will show it in VS Code, I guess. Like, there may be one file with inputs, for
example, like in addition to the 3. Um, and yeah, no need to show it here.

**[00:21:53] Speaker A:** Okay, okay, so that's it.

**[00:21:55] Speaker B:** Okay, surviving negative, I don't know what this is.

**[00:21:59] Speaker A:** Where is it?

**[00:22:04] Speaker B:** And then it says selected.

**[00:22:07] Speaker A:** This is the title of the exercise, the challenge
itself, because the challenge is about the surviving negative as example.

**[00:22:17] Speaker B:** So why do I need this one exercise selected?

**[00:22:23] Speaker A:** Where?

**[00:22:24] Speaker B:** Here. So I'm working on one exercise, right?

**[00:22:28] Speaker A:** Yeah, it's only the one exercise.

**[00:22:30] Speaker B:** Okay, so Why do I need this info that one exercise is
selected?

**[00:22:37] Speaker A:** We don't need that.

**[00:22:39] Speaker B:** This text? Yeah, I think we don't need it because we
can't like— we can just go practice.

**[00:22:44] Speaker A:** Yeah, we can't start with 2 or 3 exercises for now.
Yeah.

**[00:22:50] Speaker B:** Okay, cancel. What does it do?

**[00:22:53] Speaker A:** Cancel is like removing the chat.

**[00:22:57] Speaker B:** Uh-huh. Okay.

**[00:22:59] Speaker A:** That means you didn't like the exercise I gave to you
and you're going to start with another chat or start with another prompt and so
on.

**[00:23:07] Speaker B:** Okay. How do I know that? Yeah.

**[00:23:11] Speaker A:** How do you know? From description and the code. But we
mentioned the code, you don't need it. So the descriptions will be enough. Like
if I accept this one or not, it's really interesting thing or not.
