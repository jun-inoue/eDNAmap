library(pheatmap)
library(vegan)
library(grid)

set.seed(123)

args            <- commandArgs()
infile          <- args[6]   # "200_communityData4R_station.csv"
index_distance  <- args[7]   # "jaccard bray"
outfile.pdf     <- args[8]   # "610_out_pheatmap.pdf"


df1 <- read.csv(infile, header=T, row.names=1)

num_fontsize_col  <- 8
if (ncol(df1) < 100){
    num_fontsize_col = 6
} else if (ncol(df1) < 200) {
    num_fontsize_col = 3
} else if (ncol(df1) < 300) {
    num_fontsize_col = 2
} else if (ncol(df1) < 400) {
    num_fontsize_col = 1
} else if (ncol(df1) < 1000) {
    num_fontsize_col = 0.5
} else {
    num_fontsize_col = 0.4 # not printing
}


num_fontsize_row  <- 8
if (nrow(df1) < 50){
    num_fontsize_row = 8
} else if (nrow(df1) < 100) {
    num_fontsize_row = 5
} else if (nrow(df1) < 200) {
    num_fontsize_row = 3
} else if (nrow(df1) < 300) {
    num_fontsize_row = 2
} else {
    num_fontsize_row = 0.5
}


#### Printout
if (index_distance == "jaccard"){
    print("jaccard")
    data_binary <- as.data.frame(lapply(df1, function(x) ifelse(x > 0, 1, 0)))
    data_binary_t <- t(data_binary)

    vector_index <- rownames(df1)
    colnames(data_binary_t) <- vector_index

    pdf(outfile.pdf)
    pheatmap(data_binary_t, color = c("white", "blue"),
             show_rownames = T, 
             cluster_rows = FALSE, cluster_cols = FALSE,
             legend_breaks = c(0, 1), legend_labels = c("0", "1"),
             fontsize_row = num_fontsize_col,
             fontsize_col = num_fontsize_row
             )
    #grid.text(paste("Distance:", "Binary-converted data"), x = 0.95, y = 0.05, just = "right", gp = gpar(fontsize = 8))
    grid.text("Binary converted", x = 0.95, y = 0.03, just = "right", gp = gpar(fontsize = 8))
    dev.off()
} else {
    data_binary_t <- t(df1)
    pdf(outfile.pdf)
    pheatmap(data_binary_t, color = colorRampPalette(c("gray99", "red", "yellow", "blue"))(100),
             #fontsize = num_fontsize, 
             show_rownames = T, 
             cluster_rows = FALSE, cluster_cols = FALSE,
             fontsize_row = num_fontsize_col,
             fontsize_col = num_fontsize_row,
             cutree_rows = 3,  # 4
             )
    #grid.text(paste("Distance:", "Raw data"), x = 0.95, y = 0.05, just = "right", gp = gpar(fontsize = 8))
    grid.text("Raw data", x = 0.95, y = 0.03, just = "right", gp = gpar(fontsize = 8))
    dev.off()
}
