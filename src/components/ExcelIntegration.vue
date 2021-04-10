<template>
  <section class="container mt-5">
    <h1 class="headline text-center">Using Meals Count Directly in Microsoft Excel</h1>
    <br />
    <p>
    As part of Meals Count, we have bundled 
    a <a href="https://github.com/opensandiego/mealscount-backend/blob/main/tools/MealsCountVBAScript.bas">VBA Script</a> 
    that you can embed in your Excel document to directly run optimizations on MealsCount and have them feed back and
    update your Excel document. <strong>Note</strong> at this time this script is built for Desktop Excel for Windows and Mac,
    and may not necessarily work on Office for the Web. 
    </p>

    <p>Setting up this document requires a bit of advanced Excel which we run through on this page. However there are pre-built 
    Excel workbooks that you can use that already incorporate this functionality (and more CEP functionality) available here:</p>

    <ul>
       <li><a href="https://github.com/opensandiego/mealscount-backend/blob/main/tools/MealsCountExample.xlsm">Meals Count Example XLSM</a> (note you will need to enable editing and content to use this)</li>
       <li>(MORE COMING SOON!)</li>
    </ul>

    <h2 class="mb-3 mt-5">Adding the Meals Count VBA Script</h2>

    <h3>Step 1: Enable Developer Mode</h3>

    <p>To add the VBA Script, you will need to have Developer Mode enabled in Excel.  Go to File tab, then Options > Customize Ribbon.
        Under Customize Ribbon, and under Maint Tabs, select the Developer Check Box.
        <a href="https://support.microsoft.com/en-us/topic/show-the-developer-tab-e1192344-5e56-4d45-931b-e5fd9bea2d45">Microsoft Support Instructions</a>
    </p>

    <h3>Step 2: Download required files</h3>

    <p>Meals Count VBA requires the open source <a href="http://vba-tools.github.io/VBA-Web/">VBA Tools</a> to help it communicate with the website. 
        Please download the latest release from the following links:</p>
    
    <ul>
        <li><a target="_blank" href="https://github.com/VBA-tools/VBA-Web/releases">Download the latest release zip</a></li>
    </ul>

    <h3>Step 3: Import the files</h3>

    <p>Once you have downloaded and extracted VBA-Web, use either the <em>VBA-Web Blank</em> or the <em>VBA-Web Installer</em> sheets to install the necessary
    components in your sheet. You will only need the <strong>VBA-Web</strong> and <strong>VBA-Dictionary</strong> default components.</p>

    <p>Note you will need to enable macros, as well as go to Developer->Macro Security and check "Trust Access to the VBA Project Model" if you want to use the installer.</p>

    <p>In the Visual Basic Editor, go to <strong>File &gt; Import File</strong> and import <em>MealsCountVBAScript.bas</em>. You should also see modules installed from VBA-Tools.</p>

    <h3>Step 4: Create a MealsCount Import sheet and named range</h3>

    <p>To work, the VBA script requires a  Named Range that is 8 columns wide called "MealsCountSchools". </p>

    <p>Create the following column headers on a sheet for reference, then select a range 8 columns wide through however many schools you might have 
    in your district (e.g. <strong>A2:H101</strong> for 100 schools) and define a named range by right-clicking and selecting <strong>Define Name</strong>.
    The name <strong>must</strong> be <strong>MealsCountSchools</strong></p>

    <h4>Columns</h4>
    <table class="table">
        <tbody>
            <tr>
                <td>school_name</td>
                <td>total_enrolled</td>
                <td>total_eligible</td>
                <td>daily_breakfast_served</td>
                <td>daily_lunch_served</td>
                <td>severe_need</td>
                <td>grouping</td>
                <td>group_isp</td>
            </tr>
        </tbody>
    </table>

    <h3>Step 5: Create an Optimize Button</h3>

    <p>To trigger the optimization run, you need to add a button. Under <strong>Developer</strong> click
    <strong>Insert</strong> and then select the top left icon under <strong>Form Controls</strong>, which
    is the button. Drag out a square on the sheet and release and a window will pop up asking you to 
    assign a Macro. You should see <strong>GetGroupingsFromMealsCount</strong> if your file imports worked
    correctly. Select this and press OK.</p>

    <h3>Step 6: Add data and optimize</h3>

    <p>Now you can add school data to your rows. Column data can be referenced from other sheets in your workbook.
    Please note the following about the following columns:</p> 

    <ul>
        <li>school_name: must be unique</li>
        <li>severe_need: should be TRUE or FALSE</li> 
        <li>grouping and group_isp: clear this out to see the output of MealsCount</li>
    </ul>

    <p>Once you have added school data, press your optimize button and you should see 3 message boxes. First
        you should see one reporting that data has been sent to MealsCount. Second you should see one saying 
        data was accepted and waiting for result. The last step might take up to a few minutes (or a few seconds, 
        depending on how many schools you have), so please wait until it pops up and says that the groupings have
        been updated. You should then see the grouping and group_isp columns filled in.
    </p>

    <p>You can also create named ranges for <em>MealsCountState</em> (single cell) and <em>MealsCountDistrict</em> (Name then Code in the same column) to pass
    the state code and district name and code. These aren't required, but may influence state specific computations in the future. See the example file 
    for more specifics.</p>

    <h3>Step 7: Getting Help</h3>

    <p>In the event that you get an error or have trouble, please don't hesitate to reach out to us via the <router-link to="contact">Contact Form</router-link>. 
    You can also reference the example we provide (linked at the top of this page).</p>

  </section>
</template>
