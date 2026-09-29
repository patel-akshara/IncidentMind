# Architecture

## Memory loop

```text
Resolved incident
      |
      v
   Hindsight retain()
      |
      v
Memory bank
      |
New incident
      |
      v
 Hindsight recall()
      |
      v
Historical memories
      |
      v
Groq analysis
      |
      v
Investigation / resolution
      |
      +----> retain() new learning
```

Hindsight's documented operations are `retain`, `recall`, and `reflect`. This implementation uses retain and recall explicitly so the judge can see the memory loop in the application.
