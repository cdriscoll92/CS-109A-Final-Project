

library(foreign)
library(stringr)

can <- read.csv("~/Dropbox/Classes/CS 109A/CS 109A Final project/data/candidates.csv",
                stringsAsFactors = F)

can_clean <- data.frame(Location = NA,
                        Incumbent = NA,
                        Inc_party = NA,
                        Inc_first_elected = NA,
                        Candidate = NA,
                        Cand_party = NA)[-1,]

for(i in 1:nrow(can)){
  location_i <- can$Location[i]
  incumbent_i <- can$Incumbent[i]
  inc_party_i <- can$Party[i]
  inc_first_elected_i <- can$First_elected[i]
  
  cand_str <- can$candidates[i]
  cand_str_split <- strsplit(cand_str, "\n")[[1]]
  cand_str_names <- str_match(cand_str_split, "([^\\(]+) \\(")[,2]
  cand_str_party <- str_match(cand_str_split, "\\(([^\\)]+)\\)")[,2]
  
  df_to_bind <- data.frame(Location = location_i,
                           Incumbent = incumbent_i,
                           Inc_party = inc_party_i,
                           Inc_first_elected = inc_first_elected_i,
                           Candidate = cand_str_names,
                           Cand_party = cand_str_party)
  can_clean <- rbind(can_clean, df_to_bind)
}

can_clean$state_name <- str_match(can_clean$Location, "([A-Za-z ]+) [0-9]+")[,2]
can_clean$district_num <- str_match(can_clean$Location, "([0-9]+)")[,2]

state_abbs <- read.csv("~/Dropbox/Classes/CS 109A/CS 109A Final project/data/state_abbreviations_correspondence_table.csv",
                       sep = "\t")
can_clean <- merge(can_clean, state_abbs, by = "state_name", all.x = T)

can_clean$dist_id <- paste(can_clean$state_abb, can_clean$district_num, sep = "_")

can_clean$Cand_party_abb[grep("Democratic", can_clean$Cand_party)] <- "D"
can_clean$Cand_party_abb[grep("Republican", can_clean$Cand_party)] <- "R"
## Subsetting to exclude third-party candidates
can_clean <- can_clean[!is.na(can_clean$Cand_party_abb),]
can_clean$is_incumbent <- ifelse(as.character(can_clean$Candidate) == 
                                   as.character(can_clean$Incumbent), 1, 0)

can_clean$years_in_congress <- 0
can_clean$years_in_congress[can_clean$is_incumbent==1] <- 
  2018 - can_clean$Inc_first_elected[can_clean$is_incumbent==1]


write.csv(can_clean,
          "~/Dropbox/Classes/CS 109A/CS 109A Final project/data/candidates_cleaned.csv",
          row.names = F)

can_clean <- read.csv("~/Dropbox/Classes/CS 109A/CS 109A Final project/data/candidates_cleaned.csv")

nom <- read.csv("~/Dropbox/Classes/CS 109A/CS 109A Final project/data/NOMINATE_115.csv")

nrow(unique(nom[nom$chamber == "House",c("state_icpsr", "district_code")]))
sum(nom$chamber == "House")

house_nom <- nom[nom$chamber == "House",]
house_nom$dist_id <- paste(house_nom$state_abbrev, house_nom$district_code,
                           sep = "_")
write.csv(house_nom,
          file = "~/Dropbox/Classes/CS 109A/CS 109A Final project/data/NOMINATE_115_HOUSE.csv",
          row.names = F)

sum(table(can_clean$dist_id) == 1)
