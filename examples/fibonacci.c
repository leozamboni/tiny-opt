int
main (void)
{
  int n;
  int i;
  int t1 = 0; 
  int t2 = 1; 
  int nextTerm;

  n = 5;
  if (n == 20)
    {
      n = 0;
    }
  n = 10;

  int v = 5;
  i = 1 - 1;
  for (; i < n; i++)
    {
      nextTerm = t1 + t2;
      t1 = t2;
      t2 = nextTerm;
    }

  return nextTerm;
}
