# uncompyle6 version 2.9.10
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, Feb  6 2017, 23:53:20) 
# [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)]
# Embedded file name: Mcl_Cmd_Time_DataHandler.py


def DataHandlerMain(namespace, InputFilename, OutputFilename):
    import mcl.imports
    import mcl.data.Input
    import mcl.data.Output
    import mcl.status
    import mcl.target
    import mcl.object.Message
    mcl.imports.ImportNamesWithNamespace(namespace, 'mca.status.cmd.time', globals())
    input = mcl.data.Input.GetInput(InputFilename)
    output = mcl.data.Output.StartOutput(OutputFilename, input)
    output.Start('Time', 'time', [])
    msg = mcl.object.Message.DemarshalMessage(input.GetData())
    if input.GetStatus() != mcl.status.MCL_SUCCESS:
        errorMsg = msg.FindMessage(mcl.object.Message.MSG_KEY_RESULT_ERROR)
        moduleError = errorMsg.FindU32(mcl.object.Message.MSG_KEY_RESULT_ERROR_MODULE)
        osError = errorMsg.FindU32(mcl.object.Message.MSG_KEY_RESULT_ERROR_OS)
        output.RecordModuleError(moduleError, osError, errorStrings)
        output.EndWithStatus(input.GetStatus())
        return True
    from mcl.object.XmlOutput import XmlOutput
    xml = XmlOutput()
    xml.Start('Time')
    result = Result()
    result.Demarshal(msg)
    xml.AddTimeElement('LocalTime', result.localTime)
    xml.AddSubElementWithText('LocalTimeSeconds', '%u' % result.localTime.GetSeconds())
    xml.AddTimeElement('SystemTime', result.systemTime)
    xml.AddSubElementWithText('SystemTimeSeconds', '%u' % result.systemTime.GetSeconds())
    sub = xml.AddSubElement('TimeZone')
    sub.AddTimeElement('Bias', result.bias)
    if result.state == RESULT_STATE_STANDARD:
        sub.AddSubElementWithText('CurrentState', 'Standard')
    elif result.state == RESULT_STATE_DAYLIGHT:
        sub.AddSubElementWithText('CurrentState', 'Daylight')
    else:
        sub.AddSubElementWithText('CurrentState', 'Unknown')
    sub = xml.AddSubElement('DaylightSavingsTime')
    _writeDstInfo('Standard', result.standardBias, result.standardMonth, result.standardWeek, result.standardDay, result.standardName, sub)
    _writeDstInfo('Daylight', result.daylightBias, result.daylightMonth, result.daylightWeek, result.daylightDay, result.daylightName, sub)
    output.RecordXml(xml)
    output.EndWithStatus(mcl.target.CALL_SUCCEEDED)
    return True


def _writeDstInfo(elementName, bias, month, week, day, name, xml):
    sub = xml.AddSubElement(elementName)
    sub.AddSubElementWithText('Name', name)
    sub.AddTimeElement('Bias', bias)
    if month == 0:
        return
    child = sub.AddSubElement('ConversionDate')
    child.AddAttribute('month', '%u' % month)
    child.AddAttribute('week', '%u' % week)
    child.AddAttribute('dayOfWeek', '%u' % day)


if __name__ == '__main__':
    import sys
    try:
        namespace, InputFilename, OutputFilename = sys.argv[1:]
    except:
        print '%s <namespace> <input filename> <output filename>' % sys.argv[0]
        sys.exit(1)

    if DataHandlerMain(namespace, InputFilename, OutputFilename) != True:
        sys.exit(-1)