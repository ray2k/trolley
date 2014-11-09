import inspect

def append_module_handlers(sourceMappings, module):
    classes = inspect.getmembers(module, lambda c: inspect.isclass(c));
    for name, cls in classes:
        handledTypes = getattr(cls, "handles", None) #Handles = [FooMessage,BarMessage]

        if isinstance(handledTypes, list):
            for msgType in handledTypes:
                append_static_handler(sourceMappings, msgType, cls)
        elif isinstance(handledTypes, type): # Handles = SomeMessage
            append_static_handler(sourceMappings, handledTypes, cls)
            
    print_handler_mappings(sourceMappings)
    
def append_static_handler(sourceMappings, messageType, handlerType):    
    if messageType not in sourceMappings:
        sourceMappings[messageType] = []
    sourceMappings[messageType].append(handlerType)

def print_handler_mappings(mappings):
    for messageType in mappings:
        for subscriberType in mappings[messageType]:            
            print("Message Type", messageType.__name__, "is handled by", subscriberType.__name__)
            
def get_handled_types(handler):
    initiatedBy = getattr(handler, "initiated_by", None)
    handles = getattr(handler, "handles", None)
    
    result = []
    
    if initiatedBy != None and isinstance(initiatedBy, type):
        result.append(initiatedBy)
    if handles != None and isinstance(handles, type):
        result.append(handles)
    if handles != None and isinstance(handles, list):
        for t in handles:
            if isinstance(t, type):            
                result.append(t)
    
    result = list(set(result))
    return result
