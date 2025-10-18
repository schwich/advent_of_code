import day7

test_instructions = """\
fo RSHIFT 3 -> fq
cj OR cp -> cq
lx -> a
NOT ax -> ay
lr AND lt -> lu
hb LSHIFT 1 -> hv""".splitlines()


def test_parse_instruction():
    for instruction in test_instructions:
        instr = day7.parse_instruction(instruction)
        assert instr is day7.Instruction.NOT
