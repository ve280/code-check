//
// Created by 吴佳遥 on 2021/5/25.
//

#ifndef PROJECT2_CONSTANTS_H
#define PROJECT2_CONSTANTS_H

/*
 * Command Line Arguments Error
 */
#define INVALID_ARGUMENT_MESSAGE  "Invalid argument for random settings. Only number is accepted. The program exits"
#define OUT_OF_RANGE_MESSAGE "Random seed exceeds the range of integer. The program exits"
#define MISSING_ARGUMENT_MESSAGE  "There are missing arguments. The program exits"
#define CANNOT_OPEN_FILE_PREFIX "Cannot open the file: "

/*
 * Bot Response
 */
#define EXIT_PROMPT  "Good night. I am going to sleep"
#define STOP_BOT_FAIL  "You are not qualified to stop me"
#define COURSE_NOT_FOUND  "I don't know this course"
#define FACULTY_NOT_FOUND  "I don't know this instructor"
#define MISSING_KEYWORD "Oh, input the search keyword first..."

/*
 * Help Text
 */
#define HELP_TEXT \
"Cheat Sheet for Repeater Bot:\n"\
"Notice: Commands start with #\n"\
"   course [keyword]:     find all the courses that contain the keyword\n"\
"   instructor [keyword]:    find all the instructors that contain the keyword\n" \
"   help:    show help message\n"\
"   time:    show the time when the message was sent\n"\
"   stop:    (For bot admins only) stop the bot"

/*
 * Values that define bot's response to no-command message
 * To repeat or admire, that is a question
 */
#define REPEAT_ROLL 20
#define ADMIRE_ROLL 30
#endif //PROJECT2_CONSTANTS_H
