library(vegan)

args            <- commandArgs()
infile          <- args[6] # "200_communityData4R.csv"  # "200_communityData4R_station.csv"
index_distance  <- args[7] # "jaccard" # "bray"
outfile.pdf     <- args[8] # "620_out_nMDS.pdf"

#edat <- read.csv("200_environmentData4R.csv", header=TRUE)                # envdat.csv  KH20-9AB_env.csv


set.seed(123)

df1 <- read.csv(infile, header = TRUE, row.names=1)

num_fontsize  <- 1
if (nrow(df1) < 50){
    num_fontsize = 0.6
} else if (nrow(df1) < 100) {
    num_fontsize = 0.6
} else {
    num_fontsize = 0.5
}

#### Printout
pdf(outfile.pdf)
if (index_distance == "jaccard"){
    print("jaccard")
    dist.jc <- vegdist(df1, method="jaccard", binary = TRUE)
    res2.mds <- metaMDS(dist.jc, trace=0)
} else {
    print("bray")
    #dist_selected <- metaMDS(df1, distance=index_distance)
    # Convert lead count data to percentage
    df_percent <- sweep(df1, 1, rowSums(df1), FUN="/") * 100
    dis.bc <- vegdist(df_percent, method="bray")
    res2.mds <- metaMDS(dis.bc, trace=0)
}
print("res2.mds")
print(res2.mds)

#colors <- edat$Depth
#colors <- as.factor(colors)
##levels(colors) <- c("black", "blue", "red")
#levels(colors) <- c("magenta", "cyan", "blue", "black")
#colors <- as.character(colors)

### Regular expression to remove part of the site name
#site_names <- rownames(res2.mds$points)
#site_names <- gsub("KH20-09_KH-20-9A-", "", site_names)
#site_names <- gsub("KH20-09_KH-20-9B-", "", site_names)
#site_names <- gsub("^[^_]+_[^_]+_", "", site_names)
#rownames(res2.mds$points) <- site_names


#plot(res2.mds, display="sites")
ordiplot(res2.mds, display="sites", type="n")
#points(res2.mds, display="sites", col=colors, pch = 19)
points(res2.mds, display="sites", pch = 19)


### Env factor, Correspondece Analysis 
#env_columns <- c("Depth", "Temperature", "Salinity", "Chl_a", "Dep", "NO3", "NO2", "NH4", "PO4", "Si_OH_4", "potential_density_anomaly_surface", "Mixed_layer_depth")
#ef <- envfit(res2.mds, edat[, env_columns], permu=4999)
#ef
#plot(ef, p.max=0.05)   # 0.0002

#text(res2.mds, display="sites", adj=c(0.5,-0.5), cex = 0.5, col=colors)
text(res2.mds, adj=c(0.5,-0.5), cex = num_fontsize)

stress <- round(res2.mds$stress, 3)
string <- paste("index_distance", ",", stress)
mtext(paste("Distance:", index_distance), side = 1, line = 3, adj = 1, cex = 0.8)
mtext(paste("Stress:", stress), side = 1, line = 4, adj = 1, cex = 0.8)
dev.off()
