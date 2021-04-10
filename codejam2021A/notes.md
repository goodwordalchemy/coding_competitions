Code Jam Round 1A

# Append Sort:
My first impression is that I can use a heap for this.  

But what is a brute force way to do this, if I had all of the computational power in the world?


# Prime Time
This one is a dynamic programming problem.

One way to do this would be to output all of the combinations having balanced sums and products.  Then just choose the max of these.  

There is definitely a way to do this where you directly prioritize the max sum.

To program this one, you could start with all of the cards in the sum hand.  Then remove one card at a time for each card and put those on the product side.

# Hacked Exam
Howly Shiyit

For any row, col, the contribution of this person to this question is some kind of combined probability that they guessed T or F with the probability that they got the answer right.

Actually, an even simpler model would be to just say that each person contributes the probability that they guessed right as a vote to True or false for that answer.  

then our expected score for that question is the sum of those probabilites / N people.