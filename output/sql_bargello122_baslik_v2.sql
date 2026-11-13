update blog_posts set
  meta_title = $t$Bargello 122 Neyin Muadili? Boss Intense ile Nota Nota Karşılaştırma$t$,
  meta_description = $d$Bargello 122, Hugo Boss Boss Intense'in muadili. Bargello'nun verdiği 6 notadan 5'i Boss Intense'te var; eksik ve fazla notaları tabloda gösterdik.$d$,
  updated_at = now()
where id = '46dea4c1-17bc-446f-8609-5f24d02f2863'
returning id, meta_title;
