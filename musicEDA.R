library(sonify) 
library(tidyverse)


detention <- read_csv('wacoDetentions.csv')

detention |> 
  count(citizenship_country) |> 
  arrange(desc(n)) |> 
  View()

detention |> 
  ggplot(aes(x = stay_book_in_date_time, y = 1)) + 
  geom_jitter(alpha = .5)

detention |> 
  ggplot(aes(x = stay_book_in_date_time, y = 1:1723)) + 
  geom_segment(xend = stay_book_in_date_time, yend = stay_book_out_date_time)

detention |> 
  mutate(period = stay_book_out_date_time - stay_book_in_date_time) |> 
  ggplot(aes(period)) + 
  geom_histogram()

#each person is a note 
#note duration to detention duration 
#pitch: different keynote to different nationality 
#intensity: 
#tempo: 
#background noise: 
#duration 

#x axis people (separated by country: Latin America)
#number of people to duration 
#

 #people and how long they stay
detention |> 
  mutate(period = stay_book_out_date_time - stay_book_in_date_time) |>
  ggplot(aes(x=1:1723, y = period, color = citizenship_country)) + 
  geom_point()

detention |> 
  mutate(period = as.numeric(stay_book_out_date_time - stay_book_in_date_time)) |>
  pull(period) -> x 
  sonify(x,duration = 25, play = TRUE)#would prefer a nice hollow breeze
sonify
obj = sonify(dnorm(seq(-3,3,.1)), duration=1, play=TRUE)
obj
