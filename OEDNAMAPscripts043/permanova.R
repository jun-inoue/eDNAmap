library(vegan)

args            <- commandArgs()
infile_read     <- "200_communityData4R_station.csv"
infile_envi     <- "200_envis.csv"
# 200_envis.csv can be made from the environment sheet of .xlsx file
index_distance  <- "jaccard"            #jaccard bray
outfile.csv     <- "640_out_permanova.csv"

set.seed(123)

dat_read <- read.csv(infile_read, header = TRUE, row.names=1)
dat_env <- read.csv(infile_envi, row.names = 1)

dat_read.d <- vegdist(dat_read, method = index_distance, binary = TRUE)  # bray

# Watase
dat_read_WHB <- adonis(dat_read.d ~ dat_env$WataseHB, permutations = 999)
dat_read_WHB$aov.tab$Analysis <- "WataseHB"
dat_read_WHB$aov.tab$Distance <- index_distance

# Osumi
dat_read_OHB <- adonis(dat_read.d ~ dat_env$OsumiHB, permutations = 999)
dat_read_OHB$aov.tab$Analysis <- "OsumiHB"
dat_read_OHB$aov.tab$Distance <- index_distance

# Zone
dat_read_Z <- adonis(dat_read.d ~ dat_env$Zone, permutations = 999)
dat_read_Z$aov.tab$Analysis <- "Zone"
dat_read_Z$aov.tab$Distance <- index_distance

# WaterProp
dat_read_WP <- adonis(dat_read.d ~ dat_env$WaterProp, permutations = 999)
dat_read_WP$aov.tab$Analysis <- "WaterProp"
dat_read_WP$aov.tab$Distance <- index_distance

write.table(dat_read_WHB$aov.tab, file = outfile.csv, sep = ",", row.names = FALSE, col.names = TRUE)
write.table(dat_read_OHB$aov.tab, file = outfile.csv, sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE)
write.table(dat_read_Z$aov.tab, file = outfile.csv, sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE)
write.table(dat_read_WP$aov.tab, file = outfile.csv, sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE)

