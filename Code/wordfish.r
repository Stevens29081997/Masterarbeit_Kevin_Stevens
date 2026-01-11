
# Load packages
library(quanteda)
library(quanteda.textmodels)
library(quanteda.textplots)

# Select the corpus: Folder with all lemmatized files
input_dir <- "C:/Users/kstevens/Desktop/Privat/Uni/Master/3Semester/Data Science/Masterarbeit/Data/Corpus_lemmatized"

# List of all .txt files
files <- list.files(input_dir, pattern = "\\.txt$", full.names = TRUE)

# Read files as character vectors
docs <- sapply(files, function(f) paste(readLines(f, encoding = "UTF-8"), collapse = " "))

# Extract names of parties from file names
names(docs) <- gsub("\\.txt$", "", basename(files))

# Apply corpus to character vectors
corp <- corpus(docs)

# Tokenization & creating DFMs
toks <- tokens(corp, remove_punct = TRUE)
dfmat <- dfm(toks)

# Execute Wordfish
tmod_wf <- textmodel_wordfish(dfmat, dir = c(1, length(docs)))

summary(tmod_wf)

# Document positions of parties
party_positions <- data.frame(
  Partei = docnames(dfmat),
  Position = tmod_wf$theta,
  SE = tmod_wf$se.theta
)

print(party_positions)

# Sort parties by position (descending)
party_positions_sorted <- party_positions[order(-party_positions$Position), ]

cat("\n*** Sortierte Parteien (absteigend nach Wordfish-Position): ***\n")
print(party_positions_sorted)

# Distance matrix of party positions (with names)
positions <- party_positions$Position
names(positions) <- party_positions$Partei

dist_matrix <- dist(positions)

# Hierarchical cluster analysis
hc <- hclust(dist_matrix, method = "ward.D2")

# Save PNG file in the same folder as the files
output_png <- file.path(input_dir, "wordfish_clusterplot.png")

png(output_png, width = 1600, height = 1200, res = 200)
plot(hc,
     main = "Clusterplot der Parteien basierend auf Wordfish-Positionen",
     xlab = "Partei",
     sub = "",
     labels = party_positions$Partei,
     cex = 0.9)
dev.off()

cat("\nClusterplot gespeichert als:", output_png, "\n")

# Plot of the Wordfish scale
textplot_scale1d(tmod_wf, margin = "documents")
