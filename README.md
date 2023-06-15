# Pipedoc

Generate docs from pipeline libraries. Compatible with Gitlab CI but other yaml-based CIs should also work

## How to

1. Separate your templates into "modules" where one file contains only one template and it's variables (e.g. golang.yaml)

2. Group modules into separate directories (e.g. build)

3. Write your doc in comment at the beginning of the module's file and insert yaml document separator (---) after it. It's your module docstring which will be inlined into documentation.

4. Add comments like ```#!opt: Some awesome option``` before variables should be documented

5. ```mkdir -p docs/{raw,modules}```

6. ```python3 .```

7. Enjoy!