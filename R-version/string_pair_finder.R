library(stringr)

clean <- function(s){
    str_to_lower(iconv(s, from="UTF-8", to="ASCII//TRANSLIT//IGNORE"))
}

pair_similarity <- function(s1, s2){
  data <- matrix(sapply(str_split(s2, "", simplify = T), function(x) as.numeric(str_split(s1, "", simplify = T) == x)),
                 ncol = str_count(s2), nrow = str_count(s1),
                 dimnames = list(str_split(s1, "", simplify = T), str_split(s2, "", simplify = T)))
 
  for(i in 2:nrow(data)){
    for(j in 2:ncol(data)){
      bef <- data[i - 1, j -1]
      if(bef * data[i, j]  > 0){
        data[i, j] <- bef * 2
      }
    }
  }
  return(sum(data) / (nrow(data) * ncol(data)) )
}

get_pairs <- function(list1, list2){
  data <- as.data.frame(list2)
  for (i in list1){
    data[,i] <- sapply(list2, function(x) pair_similarity(clean(i), clean(x)))
  }
  rownames(data) <- list2
  data <- data[,-1]
  
  result <- data.frame(list2 = list2)
  for(i in 1:nrow(result)){
    result[i, "list1"] <- names(sort(data[i,],decreasing = T)[1])
    result[i, "score"] <- sort(data[i,],decreasing = T)[1]
  }
  return(result)
}