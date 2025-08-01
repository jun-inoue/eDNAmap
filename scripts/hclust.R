library(vegan)

args            <- commandArgs()
infile          <- args[6] # "200_communityData4R_station.csv"
index_distance  <- args[7] # "jaccard bray"
outfile.pdf     <- args[8] # "630_out_hclust.pdf"

set.seed(123)

df1 <- read.csv(infile, header = TRUE, row.names=1)

num_fontsize_row  <- 1.0
#distance_leaf_y  <- -1.1
if (nrow(df1) < 25){
    num_fontsize_row = 1.0
    #distance_leaf_y  <- -1.1
} else if (nrow(df1) < 50){
    num_fontsize_row = 1.0
    #distance_leaf_y  <- -0.06
} else if (nrow(df1) < 100) {
    num_fontsize_row = 0.8
} else if (nrow(df1) < 150) {
    num_fontsize_row = 0.5
    #distance_leaf_y  <- 0.05
} else {
    num_fontsize_row = 0.3
}

### Printout
if (index_distance == "jaccard"){
    dist_selected <- vegdist(df1, distance="jaccard", binary = TRUE)
} else {
    dist_selected <- vegdist(df1, distance=index_distance)
}
hc <- hclust(dist_selected, method = "ward.D2")
pdf(outfile.pdf)
plot(hc, cex=num_fontsize_row, sub = "", xlab = "")
mtext(paste("Distance:", index_distance), side = 1, line = 3, adj = 1, cex = 0.8)
dev.off()
