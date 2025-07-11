
prev_context = ['']

def get_prev_context(current_context : str = ''):
    global prev_context
    if(current_context == ''):
        context = prev_context[-1]
    else:
        context = '\n'.join(prev_context)
        if(len(prev_context) == 1 and prev_context[0] == ''):
            prev_context[0] = current_context
        else:
            prev_context.append(current_context)
    if len(prev_context) > 3:
        prev_context = prev_context[1:]
    return context