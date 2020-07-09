"""
SELECT
  *, (
    6371 * acos (
      cos ( radians(78.3232) )
      * cos( radians( latitude ) )
      * cos( radians( longitude ) - radians(65.3234) )
      + sin ( radians(78.3232) )
      * sin( radians( latitude ) )
    )
  ) AS distance
FROM users
HAVING distance < 3000
ORDER BY distance
LIMIT 0 , 20;
"""