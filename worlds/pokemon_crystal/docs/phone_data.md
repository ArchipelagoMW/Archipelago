# Guidelines for PRs that add new Phone Traps

## Technical Guidelines
- Every phone call can only be a max of 1024 bytes (1kib). This will be assured via unit test. Just be aware there is a limit.
- A line is max 18 characters long. This will be assured via unit test and validated during generation. Just be aware of the limit when writing it.
- Each section (paragraph) is up to 3 lines long. The text box will reset after each section.
- When using RIVAL or PLAYER variables, assume they are the max of 7 characters.
- We cannot add new callers. The available callers are:
   - none
   - mom
   - bikeshop
   - bill
   - elm
   - withheld
   - bank_of_mom
   - brock
   - eusine
   - out_of_area

The basic phone scripts are defined in `data/phone_data.yaml`.

Each script follows the convention:

```yaml
sample_script:
  caller: out_of_area
  script:
    - |
      The quick brown
      fox jumps over
      the lazy dog.
    - |
      The placeholders
      <player>, <rival>,
      and <POKE> may be used.
```

The script is identified as "sample_script", and the call is from "OUT OF AREA".
Each new paragraph is denoted with YAML syntax `- |` which starts a new array member as a multi-line literal scalar.
It is strongly recommended to use this for readability and to avoid accidental YAML special behavior.

The placeholder tags have these effects:

| Placeholder | Effect         | Size |
| ----------- | -------------- | ---- |
| \<player\>  | Player name    | 7    |
| \<rival\>   | Rival name     | 7    |
| \<POKE\>    | Literal "POKÉ" | 4    |

## Content Guidelines
- Look at the original 16 phone traps. We want the kind of humor to be adjacent to that.
- The humor has to be funny without context. Except Pokémon humor - you may assume everyone knows all Pokémon lore.
- The phone traps do not have to be Pokémon-related.
- They have to be SFW (appropriate for 17 years old).
- They *can* contain references to copyrighted content. They *cannot* contain copyrighted content.

# Submission Considerations
- Only submit ONE Phone Trap per Pull Request
- A submission has to be approved by at least 5 users by giving a "Thumbs Up" reaction on the PR
- Two of these approvals need to be @gerbiljames and @palex00
- This requirement may change as we learn with the system
