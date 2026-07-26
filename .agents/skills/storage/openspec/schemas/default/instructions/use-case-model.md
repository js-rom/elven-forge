## Use Case Purpose

- The essense is discovering and recording functional requirements by writing **text** stories of using a system to fulfill user goals; that is, cases of use. 
- Use cases enphasize the  user goals and perspective. The try to aswer questions as "Who is using the system, what are their typical scenarios of use, and what are their goals?" **user centric emphasis**.
- A use case defines a **contract of how system will behave**.

## Use Case influence

The use cases can in turn influence many other analysis, design, implementation, project management, and test artifacts. Sample UP artifact influence with an enphasis on text use cases

 ### Requirements

- Use Case Diagram  helps to obteain use case names for Use Case Text. 
- Use Case Text helps to identify system events for System Sequence Diagrams. 
- System Sequence Diagrams help to identify system operations for Operation Contracts. Communication Diagrams help to identify operations for Class Diagrams. Class Diagrams help to identify code modules for implementation. Use Case Text also helps to identify test scenarios for test case design.

 ### Business Modeling

- Domain Model objects, attributes and asociations are influenced by the use cases as they help to identify the key concepts and relationships in the problem domain.

### Design

- Design Models (e.g., Class Diagrams, Sequence Diagrams) are influenced by the use cases as they help to identify the necessary system components and their interactions.

### Other secondary requirement artifacts

- Vision scope, goals, actors and features are influenced by the use cases as they help to clarify the system's intended functionality and user interactions.
- Glosary terms, attributes and validation rules are influenced by the use cases as they help to identify key concepts and their properties in the problem domain.
- Suplementary specification non-funcitional requirements and queality attributes are influenced by the use cases as they help to identify the necessary system qualities and constraints.
    
## Definitions

- An **actor** is something with behavior, such as a person (identified by role), computer system, or organization. For example: a cashier.
- A **scenario** is a specific sequence of actions and interactions between actors and the system; it is also called a use case instance. It is one particular story of using a system, or one path through the use case, for example:
    - the scenario of succesfully purchasing items with cash,
    - or the scenario of failing to purshase items because of a credit payment denial.
- **use case** is a collection of related success and failure scenarios that describe an actor using a system to support a goal.s

## Three kind of actors

An actor is something with behavior inckuding the system under discusion (SuD) itself when it calls upon the services of other systems.

- **Primary actor** has user goals fulfilled through using services of the SuD
- **Suporting actor** provides a service (for example, information) to the SuS.
- **Offstage actor** has an interest in the beavior of the use case, for example a government tax agency.

## Use case Formats

### brief
Terse one paragraph summary, usually of the main success scenario. 
e.g: "**purchase.** The cashier uses the POS system to record each pur-chased item. The system presents a running total and line-item details. The customer enters payment information, which the system validates and records. The system updates inventory. The customer receives a receipt from the system and then leaves with the items." 

**when:** during early requirement analysis, to get a quick sense of subject and scope.

### fully dressed

Fully dressed use cases show more detail and are structured, they dig deeper. All steps and variations are written in detail and there are supporting sections.

#### Scope

Bound the system (or systems) under design.

#### Level

- A user-goal level use case is the common kind that describe the scenarios to fulfill the goals of a primary actor to get work done.
- A sub-function level use case describes sub-steps require to suport a user goal, and is usually created to factor out duplicate substeps shared by several reglar use cases.

#### Primary Actor

The principal actor that calls upon system services to fulfill a goal

#### Stake Holders and Interest List **(important)**

The use case, as the contract for behavior, captures **all and only** the beaviors related to satifying the stakeholders' interests.
Stake Holders and Interest List answer the question: What should be in the use case? and the answer is: That wich satisfies all the stakeholders' interests.

#### Preconditions and Success Guarantees (Postconditions)

Do not write Preconditions and Success Guarantees unless you are stating something non-obvious and noteworthy to hel the reader gain insight.

- precondtions: state what must be true before a scenario is begun in the use case.
- postconditions: state what must be true on successful completion od the use case. The guarantee should meet the needs of **all stakeholders**.

#### Main Success Scenario and Steps

It describes a typical success path that satisfies the interests of the stakeholders. Note that it often **notinclude any conditions**  or branching. Try to **defer all conditional handling** to the Extensions section.

the scenarion record steps, of which there are three kinds:
1. An interaction between actors.
2. A validation (usually by the system)
3. A state change by the system.

**RULES**
- write the steps as a markdown ordered numeric list
- Step one of a use case usually indicates the trigger event that start the scenario.
- Capitalize the actor's name
- to indicate repetition use: `Actor repeats step(s) {{intial-step-number}}-{{final-step-number}} until {{condition}}` 
for example:
```markdown
Main Success Scenario:
1. Customer arrives at POS checkout with items to purshase.
2. Cashier starts a new sale.
3. Cashier enters item identifier.
4. ...
Cashier repeats steps 3-4 until done
5. ...
```

#### Extensions

- Extension indicates all other scenarios or branches, both success and failure.
- It is common that extensions section is considerably longer and more complex than Main Success Scenario.
- The combination of the Main Success Scenario and extension scenarios should satisfies "nearly" all the interests of tha stakeholders. Some interest may best be captured as non-functional requirementes.
- Extensions have two parts: the condition and the handling.
- when possible, write the condition as something tha can be detected by the system or an actor. for emple:
prefer:
`step 5a. System detect failure to communicate with external tax calculation system devide`
over:
`step 5a. External tax calculation system not working`
- Extension handeling can be summarize in one step, or include a sequence to indicate that a condition can arise within a range of steps, e.g., 
```md
- step 3-6a: Customer ask Cashier to remove an item from the purshase:
    - step 1. Cashier enters the item identifier ...
```
- At the end of extension andling, by default he scenario merges back with the main success scenario, unless the extension indicates otherwise.
- If a particular extension point is too complex can be motivation to express the extension as a separate use case.
- if it is desirable to describe an extension condition as possible during any or at least most steps, the labels `*a, *b, ...` can be used.
- Someties, a use case banches to perfor another use case, for exaple the story "find product help" is a distinct use case that is someties performed while within Process Sale. use a link to the use case.
- Extension scenarios ara branches from the main success scenario, and so can be notated with respect to its steps 1...N. Extensions for the same main scenario (e.g. 1) will be notated as `- Step {{#}}{{first-alphabet-letter}}. {{condition}}`, `- Step {{#}}{{second-alphabet-letter}}. {{condition}}`, etc. After condition is identified, the response steps list follows tab indented as  `- Step {{#}}. {{response}}`, `- Step {{#}}. {{response}}`, etc. for example:
```md
Main Success Scenario:
1. Customer arrives at POS checkout with items to purshase.
2. Cashier starts a new sale.
3. Cashier enters item identifier.

Extensions:
- step 3a. Invalid Item ID (not found in system).
    - step 1. System signals error and rejects entry.
    - step 2. Cashier respond to the error:
        - step 2a. There is a human-readeable item ID (e.g., a numeric UPC )
            - step 1. Cashier manually enters the item ID.
            - step 2. System displays description and price.
                - step 2a.Invalid item ID: System signals error. Cashier tries alternate method.
                - step 2b. There is n item ID, but there is a price on tag:
                    - step 1. ...
                    - step 2. ...
                - step 2c. ....
```

full use case exaple:

```markdown
## Use Case UC1: Process Sale

**Scope:** NextGen POS application  
**Level:** user goal  
**Primary Actor:** Cashier  

### Stakeholders and Interests:

- **Cashier:** Wants accurate, fast entry, and no payment errors, as cash drawer shortages are deducted from his/her salary.  
- **Salesperson:** Wants sales commissions updated.  
- **Customer:** Wants purchase and fast service with minimal effort. Wants easily visible display of entered items and prices. Wants proof of purchase to support returns.  
- **Company:** Wants to accurately record transactions and satisfy customer interests. Wants to ensure that Payment Authorization Service payment receivables are recorded. Wants some fault tolerance to allow sales capture even if server components (e.g., remote credit validation) are unavailable. Wants automatic and fast update of accounting and inventory.  
- **Manager:** Wants to be able to quickly perform override operations, and easily debug Cashier problems.  
- **Government Tax Agencies:** Want to collect tax from every sale. May be multiple agencies, such as national, state, and county.  
- **Payment Authorization Service:** Wants to receive digital authorization requests in the correct format and protocol. Wants to accurately account for their payables to the store.  

### Preconditions:
Cashier is identified and authenticated.

### Success Guarantee (or Postconditions):
- Sale is saved.  
- Tax is correctly calculated.  
- Accounting and Inventory are updated.  
- Commissions recorded.  
- Receipt is generated.  
- Payment authorization approvals are recorded.
## Main Success Scenario (or Basic Flow):

1. Customer arrives at POS checkout with goods and/or services to purchase.  
2. Cashier starts a new sale.  
3. Cashier enters item identifier.  
4. System records sale line item and presents item description, price, and running total. Price calculated from a set of price rules.  

   Cashier repeats steps 3-4 until indicates done.  

5. System presents total with taxes calculated.  
6. Cashier tells Customer the total, and asks for payment.  
7. Customer pays and System handles payment.  
8. System logs completed sale and sends sale and payment information to the external Accounting system (for accounting and commissions) and Inventory system (to update inventory).  
9. System presents receipt.  
10. Customer leaves with receipt and goods (if any).  

## Extensions (or Alternative Flows):

- *a. At any time, Manager requests an override operation:
    - step 1. System enters Manager-authorized mode.  
    - step 2. Manager or Cashier performs one Manager-mode operation (e.g., cash balance change, resume a suspended sale on another register, void a sale, etc.).  
    - step 3. System reverts to Cashier-authorized mode.  

- *b. At any time, System fails:
    To support recovery and correct accounting, ensure all transaction sensitive state and events can be recovered from any step of the scenario.  
    - step 1. Cashier restarts System, logs in, and requests recovery of prior state.  
    - step 2. System reconstructs prior state.  
        - step 2a. System detects anomalies preventing recovery:  
            - step 1. System signals error to the Cashier, records the error, and enters a clean state.  
            - step 2. Cashier starts a new sale.  

- step 1a. Customer or Manager indicate to resume a suspended sale:
    - step 1. Cashier performs resume operation, and enters the ID to retrieve the sale.  
    - step 2. System displays the state of the resumed sale, with subtotal.  
        - step 2a. Sale not found:  
            - step 1. System signals error to the Cashier.  
            - step 2. Cashier probably starts new sale and re-enters all items.  

- step 3. Cashier continues with sale (probably entering more items or handling payment).  

- step 2-4a. Customer tells Cashier they have a tax-exempt status:
    - step 1. Cashier verifies, and then enters tax-exempt status code.  
    - step 2. System records status (which it will use during tax calculations).  

- step 3a. Invalid item ID (not found in system):
    - step 1. System signals error and rejects entry.  
    - step 2. Cashier responds to the error:  
        - step 2a. There is a human-readable item ID (e.g., a numeric UPC):  
            - step 1. Cashier manually enters the item ID.  
            - step 2. System displays description and price.  
                - step 2a. Invalid item ID: System signals error. Cashier tries alternate method.  
        - step 2b. There is no item ID, but there is a price on the tag:  
            - step 1. Cashier asks Manager to perform an override operation.
            - step 2. Manager performs override.  
            - step 3. Cashier indicates manual price entry, enters price, and requests standard taxation for this amount (because there is no product information, the tax engine can't otherwise deduce how to tax it).  
        - step 2c. Cashier performs [Find Product Help](path to Find Product Help use case) to obtain true item ID and price.  
        - step 2d. Otherwise, Cashier asks an employee for the true item ID or price, and does either manual ID or manual price entry (see above).

- step 3b. There are multiple of same item category and tracking unique item identity not important (e.g., 5 packages of veggie-burgers):
    - step 1. Cashier can enter item category identifier and the quantity.

- step 3c. Item requires manual category and price entry (such as flowers or cards with a price on them):
    - step 1. Cashier enters special manual category code, plus the price.

- step 3-6a. Customer asks Cashier to remove (i.e., void) an item from the purchase:
    This is only legal if the item value is less than the void limit for Cashiers, otherwise a Manager override is needed.  
    - step 1. Cashier enters item identifier for removal from sale.  
    - step 2. System removes item and displays updated running total.  
        - step 2a. Item price exceeds void limit for Cashiers:  
            - step 1. System signals error, and suggests Manager override.  
            - step 2. Cashier requests Manager override, gets it, and repeats operation.

- step 3-6b. Customer tells Cashier to cancel sale:
    - step 1. Cashier cancels sale on System.

- step 3-6c. Cashier suspends the sale:
    - step 1. System records sale so that it is available for retrieval on any POS register.  
    - step 2. System presents a "suspend receipt" that includes the line items, and a sale ID used to retrieve and resume the sale.  

- step 4a. The system supplied item price is not wanted (e.g., Customer complained about something and is offered a lower price):
    1. Cashier requests approval from Manager.  
    2. Manager performs override operation.  
    3. Cashier enters manual override price.  
    4. System presents new price.  

- step 5a. System detects failure to communicate with external tax calculation system service:
    - step 1. System restarts the service on the POS node, and continues.  
        - step 1a. System detects that the service does not restart:  
            - step 1. System signals error.  
            - step 2. Cashier may manually calculate and enter the tax, or cancel the sale.  

- step 5b. Customer says they are eligible for a discount (e.g., employee, preferred customer):
    1. Cashier signals discount request.  
    2. Cashier enters Customer identification.  
    3. System presents discount total, based on discount rules.  

- step 5c. Customer says they have credit in their account, to apply to the sale:
    1. Cashier signals credit request.  
    2. Cashier enters Customer identification.  
    3. System applies credit up to price = 0, and reduces remaining credit.  

- step 6a. Customer says they intend to pay by cash but don’t have enough cash:
    - step 1. Cashier asks for alternate payment method.  
        - step 1a. Customer tells Cashier to cancel sale. Cashier cancels sale on System.

- step 7a. Paying by cash:
    - step 1. Cashier enters the cash amount tendered.
    - step 2. System presents the balance due, and releases the cash drawer.
    - step 3. Cashier deposits cash tendered and returns balance in cash to Customer.
    - step 4. System records the cash payment.

- step 7b. Paying by credit:
    - step 1. Customer enters their credit account information.
    - step 2. System displays their payment for verification.
    - step 3. Cashier confirms.
        - step 3a. Cashier cancels payment step:
            - step 1. System reverts to “item entry” mode.
    - step 4. System sends payment authorization request to an external Payment    Authorization Service System, and requests payment approval.
        - step 4a. System detects failure to collaborate with external system:
            - step 1. System signals error to Cashier.
            - step 2. Cashier asks Customer for alternate payment.
    - step 5. System receives payment approval, signals approval to Cashier, and releases cash drawer (to insert signed credit payment receipt).
    - step 5a. System receives payment denial:
        - step 1. System signals denial to Cashier.
        - step 2. Cashier asks Customer for alternate payment.
    - step 5b. Timeout waiting for response.
        - step 1. System signals timeout to Cashier.
        - step 2. Cashier may try again, or ask Customer for alternate payment.
    - step 6. System records the credit payment, which includes the payment approval.
    - step 7. System presents credit payment signature input mechanism.
    - step 8. Cashier asks Customer for a credit payment signature. Customer enters signature.
    - step 9. If signature on paper receipt, Cashier places receipt in cash drawer and closes it.

- step 7c. Paying by check…

- step 7d. Paying by debit…

- step 7e. Cashier cancels payment step:
    - step 1. System reverts to “item entry” mode.

- step 7f. Customer presents coupons:
    - step 1. Before handling payment, Cashier records each coupon and System reduces price as appropriate. System records the used coupons for accounting reasons.
        - step 1a. Coupon entered is not for any purchased item:
            - step 1. System signals error to Cashier.

- step 9a. There are product rebates:
    - step 1. System presents the rebate forms and rebate receipts for each item with a rebate.

- step 9b. Customer requests gift receipt (no prices visible):
    - step 1. Cashier requests gift receipt and System presents it.

- step 9c. Printer out of paper.
    - step 1. If System can detect the fault, will signal the problem.
    - step 2. Cashier replaces paper.
    - step 3. Cashier requests another receipt.
```

### Special Requirements

if a non-functional requirement, queality attribute, or constraint relates specifically to a use case, record it with the use case.

### Technology and Data Variations List

- it is skillfull to avoid premature design decisions, but some times they are obvious or unavoidable, especially concerning input/output technologies.

## Guidelines

### Esential UI-Free Style

In a essential writing style, the narrative is expressed at the level of the user's **intentions** ans system's **responsabilities** rather than their concrete actions. They remain free of technology and mechanism details, especially those related to the UI.

## Write Terse Use Cases

Write terse use cases. Delete "noise" words.

## Write Black-Box Use Cases

Black-box use cases do not describe the internal workings of the system, its components, or design. Rather, the system is describes as having responsabilities, which is a comon unifying metaphorical thee in object-oriented thinking-software elements have responsabilities and collaborate with other elements that have responsabilities.

You must define what the system must do without deciding how it will do it.

## Take an Actor and Actor-Goal Perspective.

- Write requirements focusing on the users or actors of a system, asking about their goals and typical situations.
- Focus on understanding what the actor considers a valuable result.

## How to Find Uses Cases

The procedure is:

### Step 1: Choose the system Boundary

If the definition of the boundary of the system under design  is not clear, it can be clarirified by further definition of what is outside.

### Step 2 and 3: Find primary actors and goalss

- Brainstorm the primary actors first, as this sets up the framework for further investigation. 
- In addition to the obvious primary actors and goals, this questions can help identify others that may be missed:
    - Who starts ans stops the system?
    - Who does user and security management?
    - Who does system administration?
    - is "time" an actor because the system does soething in response to a time event?
    - Is there a monitoring process that restarts the system if it fails?
    - How are software updates handled? Push or pull update?
    - In addtion to human primary actors, are there any external software or robotic systems that call upon services of the system?
    - Who evaluates system activity or performace?
    - Who evaluates logs? Are they remotely retrieved?
    - Who gets notified when there are errors or failures?
- Write an actor-goal list first to the vision artifact, review and refine in pairs with the user, then draw the use case diagram.
- The viewpoint of use case modeling is to find actors and their goals, and create solutions that produce a result of value. Rather than asking "What are the tasks?" start by asking "Who uses the system and what are their goals?"
- The primary actor depends on the system boundary of the system under design, and who we are primarily designing the system for.

### Step 4: Defin Use Cases

- In general, define one use case for each user goal.
- Name the use use case similar to the user goal.
- Start the name of use cases with a verb.
- A common exception to one use case per goal is to collapse CRUD separate goals into one CRUD use case, idiomaatically called Manage <X>

## Finding Useful Use Cases

There are several rules of thub to find useful level to express use case for application requirement analysis:

### The Boss Test

Use cases must achieve results of measurable value. For example, if you are all day loggin in, your boss wouldn't be happy,; they are not results of measurable value to your boss.

## The EBP Test

Focus in use cases that reflects Elementary Business Process (EBP).

Elementary Business Process (EBP): A task performed by one person in one place at one tie, in response to a businnes event, which adds easurable business value and leaves the data in a consistent state, e.g., Approve Credit or Price Order.

## The Size Test

A use case is very seldom a single action or step.

## Use case Diagrams

- Draw a simple use case diagram in conjuction with an actor-goal list.
- show computer system actors with alternaste notatio to human actors, use the class box.
- For a use case context diagram, limit the use cases to user-goal level use cases.
- primary actors on the left
- supporting actors on the right.

## When Not to use Use Cases

Use cases are not a natural fit for application servers, database productos, and other middleware or back-end systems need to be primarily considered and evolve in terms of features (e.g., "we need Web Services support in the next release"). Use features insted. 


