# Before starting, make sure you have opened a new terminal and typed: radian
# To run the entire script, type: Ctrl+Shift+S, for one line simply Ctrl+Enter
# To modify linter try this page: https://lintr.r-lib.org/articles/lintr.html#configuring-linters

# Study 02 data series
steps_to_conv_sect2U_condUI <- c(36, 38, 43, 42, 41, 36, 43, 38, 39, 36, 41, 36) # nolint
steps_to_conv_sect2U_condIU <- c(36, 41, 36, 59, 36, 41, 42, 36, 36, 60, 36, 36) # nolint

steps_to_conv_sect2I_condUI <- c(12, 10, 15, 12, 20, 11, 40, 15, 12, 10, 18, 12) # nolint
steps_to_conv_sect2I_condIU <- c(10, 14, 11, 58, 11, 15, 23, 11, 19, 21, 9, 13) # nolint


# Study 02 Wilcoxon Rank Sum and Signed Rank Stats Analyses

# TEST 1: Steps to converge between section 2U uninformed and section 2I informed under condition UI
# Expect: significant improvement 
dat_steps_to_conv_condUI <- data.frame(value = c(steps_to_conv_sect2I_condUI,steps_to_conv_sect2U_condUI), 
                  condition = rep(c("steps_to_conv_sect2I_condUI","steps_to_conv_sect2U_condUI"), each=12))
boxplot(value ~ condition, data = dat_steps_to_conv_condUI, col = "#00b324", main = "Steps to converge [sect2U Uninformed]~[sect2I Informed] for condUI", ylab = "Steps", xlab = "Condition")
wilcox.test(steps_to_conv_sect2U_condUI, steps_to_conv_sect2I_condUI, alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = 0.95)
#OLD: wilcox.test(value ~ condition, data = dat_steps_to_conv_condUI, alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = 0.95)


# TEST 2: Steps to converge between section 2U uninformed and section 2I informed under condition IU
# Expect: significant improvement 
dat_steps_to_conv_condIU <- data.frame(value = c(steps_to_conv_sect2I_condIU,steps_to_conv_sect2U_condIU), 
                  condition = rep(c("steps_to_conv_sect2I_condIU","steps_to_conv_sect2U_condIU"), each=12))
boxplot(value ~ condition, data = dat_steps_to_conv_condIU, col = "#00b324", main = "Steps to converge [sect2U Uninformed]~[sect2I Informed] for condIU", ylab = "Steps", xlab = "Condition")
wilcox.test(steps_to_conv_sect2U_condIU, steps_to_conv_sect2I_condIU, alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = 0.95)
#OLD: wilcox.test(value ~ condition, data = dat_steps_to_conv_condIU, alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = 0.95)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# TESTING HOW THINGS WORK
# Shorter way to do the test. Your ranked value will end up as the lower of the two in this case.
# wilcox.test(accuracy_before_libA_condUI, accuracy_after_libA_condUI, alternative = "two.sided", exact = FALSE, conf.int = TRUE, conf.level = 0.95)

# test_A <- c(1, 2, 4, 4) # nolint
# test_B <- c(4, 6, 7, 8) # nolint

# dat_testing <- data.frame(value = c(test_A,test_B), 
#                   condition = rep(c("test_A","test_B"), each=4))
# boxplot(value ~ condition, data = dat_testing, col = "#00b324", main = "Testing how Wilcoxon Rank works", ylab = "Values", xlab = "Condition")
# wilcox.test(value ~ condition, data = dat_testing, alternative = "greater", exact = FALSE, conf.int = TRUE, conf.level = 0.95)
# wilcox.test(test_A, test_B, alternative = "greater", exact = FALSE, conf.int = TRUE, conf.level = 0.95)

# W = the number of times that a value in the first sample is larger than a value in the second sample (or vice versa) where ties are broken by assigning 0.5 to each value in the tie.
# The alternative hypothesis can be either two.sided, greater or less. two.sided is the default. 
# If alternative is two.sided, then the null hypothesis is that the two distributions are the same, and the alternative is that they are different. 
# If alternative is less, then the null hypothesis is that the first distribution stochastically dominates the second, and the alternative is that the first distribution does not stochastically dominate the second. 
# If alternative is greater, then the null hypothesis is that the first distribution is stochastically dominated by the second, and the alternative is that the first distribution is not stochastically dominated by the second.