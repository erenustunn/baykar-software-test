*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${URL}    https://baykartech.com

*** Test Cases ***
Click All Elements And Verify
    Open Browser    ${URL}    Chrome
    Maximize Browser Window


    ${total_elements}=    Get Length    //a

    FOR    ${index}    IN RANGE    ${total_elements}
        ${elements}=    Get WebElements    //a
        ${element_count}=    Get Length    ${elements}


        Run Keyword If    ${index} < ${element_count}    Click And Verify Element    ${elements}    ${index}
    END
    Close Browser


*** Keywords ***
Click And Verify Element
    [Arguments]    ${elements}    ${index}
    ${element}=    Get From List    ${elements}    ${index}

    Wait Until Element Is Visible    ${element}    timeout=5s
    Wait Until Element Is Enabled    ${element}    timeout=5s


    Wait Until Keyword Succeeds    3 times    2s    Click Element    ${element}

    ${title}=    Get Title
    Should Not Be Empty    ${title}
    Go Back
    Sleep    2s


#######################################################################
##NOTLAR##
##1) Kodu çalıştırmak için terminale robot komutunu yazın. --> "robot navbar_otomasyon.robot#