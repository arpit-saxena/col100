exception emptyList

fun empty([]) = true
  | empty(a::ls) = false;

fun head([]) = raise emptyList
  | head(a::ls) = a;

fun tail([]) = raise emptyList
  | tail(a::ls) = ls;

fun attach(a, ls) = a::ls;
