# ER Diagram

```text
+--------------------+        1       N       +-------------------------+
| IMAGE / ANALYSIS   |----------------------<| ANALYSIS_HISTORY        |
+--------------------+                        +-------------------------+
| analysis_id (PK)   |                        | id (PK)                 |
| filename            |                        | filename                |
| created_at          |                        | candidate_matches       |
+--------------------+                        | verified_matches        |
                                              | suspicious_regions      |
                                              | score                   |
                                              | created_at               |
                                              +-------------------------+
```
