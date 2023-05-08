#!/usr/bin/env python3

import sys
import re

normal = 'normal'
nested = 'nested'
_number_match = re.compile('\s*(-?\d*(\.?)\d+)\s*')

debug = __name__ == '__main__'
debug = False


def parse(argv=tuple(sys.argv[1:]), parse_types=True, begin='--'):
    if debug:
        print(f'parsing {argv!r}')
        # pass
    prefix_len = len(begin)
    argv = list(argv)

    args = None
    kwargs = {}
    next_kwarg = next(
        (
            i
            for i in range(len(argv))
            if argv[i].startswith(begin) or argv[i].endswith(begin)
        ),
        None,
    )
    args = parse_lists(argv[:next_kwarg])
    if debug:
        print(f'Args after assignment: {args!r}')
    del argv[:next_kwarg]
    while argv:
        kwarg = argv.pop(0)
        if kwarg.endswith(begin):
            kwarg = kwarg[:-prefix_len]
            kwarg_type = nested
            end_kwarg = f'{begin}{kwarg}{begin}'
            if end_kwarg not in argv:
                raise Exception(f'nested kwarg {kwarg} never ended')
        elif kwarg.startswith(begin):
            kwarg = kwarg[prefix_len:]
            kwarg_type = normal
        next_kwarg = next(
            (
                i
                for i in range(len(argv))
                if (
                    kwarg_type == normal
                    and (argv[i].startswith(begin) or argv[i].endswith(begin))
                )
                or (kwarg_type == nested and argv[i] == end_kwarg)
            ),
            None,
        )
        if kwarg_type == nested:
            arg_val, kwarg_val = parse(argv[:next_kwarg], parse_types, begin)
            argv.pop(next_kwarg or -1)
            del argv[:next_kwarg]
            if kwarg == '':
                args.append(kwarg_val)
                next_args, next_kwargs = parse(argv, parse_types, begin)
                args.extend(next_args)
                kwargs.update(next_kwargs)
                del argv[:]
            else:
                kwargs.update({kwarg: kwarg_val})
        elif kwarg_type == normal:
            kwarg_val = parse_lists(argv[:next_kwarg])
            del argv[:next_kwarg]
            if len(kwarg_val) == 0:
                if kwarg.startswith('no-'):
                    kwarg_val = False
                    kwarg = kwarg[3:]
                else:
                    kwarg_val = True
            elif len(kwarg_val) == 1:
                kwarg_val = kwarg_val[0]
            else:
                kwarg_val = parse_lists(kwarg_val, begin)
            kwargs.update({kwarg: kwarg_val})
    return args, kwargs


def nested_parse(*args, **kwargs):
    print(
        '\x1b[1mYou are using nested_parse, which has been deprecated.\x1b[0m',
        file=sys.stderr,
    )
    return parse(*args, **kwargs)


def parse_lists(argv=tuple(sys.argv[1:]), begin='--', *, r=False):
    prefix_len = len(begin)
    argv = list(argv)
    if debug:
        print(f'\nparsing list {argv!r}')
        # pass

    args = find_end_nest(argv, '[', ']')
    for arg, i in zip(args, range(len(args))):
        if isinstance(arg, list):
            args[i] = parse_lists(arg, begin, r=True)
        else:
            args[i] = parse_type(arg)
    return args

    """
  if '[' not in argv:
    return [parse_type(e) if e not in ('[[', ']]')
      else ('[' if e == '[[' else ']') for e in argv]
  args = argv[:argv.index('[')]
  argv = argv[argv.index('['):]
  
  nest_depth = 0
  start = 1
  for item, i in zip(argv, range(len(argv))):
    if item == '[':
      nest_depth += 1
    elif item == ']':
      nest_depth -= 1
    if item == ']' and nest_depth == 0:
      print(f'list is {", ".join(map(str, argv[start:i]))}')
      args.append(parse_lists(argv[start:i], begin, r=True))
      start = i+2
  args = [parse_type(e) if e not in ('[[', ']]')
      else ('[' if e == '[[' else ']') for e in args]
  return args[0] if len(args) == 1 and r else args
  """


def replace_escapes(argv, open_char, close_char, escapes):
    return [
        e
        if e not in escapes
        else (open_char if e == escapes[0] else close_char)
        for e in argv
    ]


def find_end_nest(argv, open_char, close_char, escapes=()):
    argv = list(argv)
    escapes = list(escapes)
    if not escapes:
        escapes.append('\\' + open_char)
    if len(escapes) < 2:
        escapes.append('\\' + close_char)
    if open_char not in argv:
        return replace_escapes(argv, open_char, close_char, escapes)

    args = replace_escapes(
        argv[: argv.index(open_char)], open_char, close_char, escapes
    )
    del argv[: argv.index(open_char)]

    nest_depth = 0
    start = 1
    for item, i in zip(argv, range(len(argv))):
        if item == open_char:
            nest_depth += 1
        elif item == close_char:
            nest_depth -= 1
        if item == close_char and nest_depth == 0:
            if debug:
                # print(f'end nest is {argv[start:i]}')
                pass
            args.append(
                replace_escapes(argv[start:i], open_char, close_char, escapes)
            )
            start = i + 2
        elif nest_depth == 0:
            args.append(item)
            start = i + 2
    if nest_depth != 0:
        raise Exception(f'nest_depth of {nest_depth} after exausting list')
    return args


def parse_args(argv=tuple(sys.argv[1:]), begin='--'):
    prefix_len = len(begin)
    argv = list(argv)

    args = None
    kwargs = {}
    while argv:
        next_kwarg = next(
            (
                i
                for i in range(0 if args is None else 1, len(argv))
                if argv[i].startswith(begin)
            ),
            None,
        )
        if args is None:
            args = argv[:next_kwarg]
            del argv[:next_kwarg]
        else:
            kwarg = argv[1:next_kwarg]
            del argv[1:next_kwarg]
            if len(kwarg) == 0:
                kwarg = True
            elif len(kwarg) == 1:
                kwarg = kwarg[0]
            kwargs.update({argv[0][prefix_len:]: kwarg})
            del argv[0]
    return args or [], kwargs


def parse_type(value):
    if not isinstance(value, str):
        return value
    is_num = _number_match.fullmatch(value)
    if is_num:
        if is_num[2]:
            return float(is_num[1])
        else:
            return int(is_num[1])
    true_vals = ('true', 't')
    false_vals = ('false', 'f')
    lowered = value.lower()
    if lowered in true_vals:
        return True
    elif lowered in false_vals:
        return False
    elif lowered == 'none':
        return None
    return value


if __name__ == '__main__':
    from json import dumps, loads

    # print(sys.argv)
    globs = globals()
    if sys.argv[1] in globs:
        args, kwargs = globs[sys.argv[1]]()
    else:
        # pass
        args, kwargs = parse()
    print(
        f'args:\n{dumps(args, indent=2)}\nkwargs:\n{dumps(kwargs, indent=2)}'
    )
    # print(args[0])
    # print(*(args[0][i:i+20] for i in range(0, len(args[0]), 20) if '"' in args[0][i:i+20]), sep='\n')
    # print(loads(args[0]))
    # [
    #     'py/argv_parse.py',
    #     '1',
    #     '2',
    #     '3',
    #     ['x', 'y', 'z', 'true'],
    #     ['[', '--', '--true_k', '--off-false_k', '----'],
    # ]
    # print('end nest []:', dumps(find_end_nest(sys.argv, '[', ']'), indent=2))
    # print(
    #     'end nest --:', find_end_nest(sys.argv, '--', '----', ('\--', '\----'))
    # )
