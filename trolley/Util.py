import inspect

def append_module_handlers(sourceMappings, module):
    classes = inspect.getmembers(module, lambda c: inspect.isclass(c));
    for name, cls in classes:
        handledTypes = getattr(cls, "handles", None) #Handles = [FooMessage,BarMessage]

        if isinstance(handledTypes, list):
            map(append_static_handler, [((sourceMappings, msgType) for msgType in handledTypes)])
            #for msgType in handledTypes:
                #append_static_handler(sourceMappings, msgType, cls)
        elif isinstance(handledTypes, type): # Handles = SomeMessage
            append_static_handler(sourceMappings, handledTypes, cls)
            
def append_static_handler(sourceMappings, messageType, handlerType):    
    if messageType not in sourceMappings:
        sourceMappings[messageType] = []
    sourceMappings[messageType].append(handlerType)

def print_handler_mappings(mappings):
    for messageType in mappings:
        for subscriberType in mappings[messageType]:            
            print("Message Type", messageType.__name__, "is handled by", subscriberType.__name__)
            
