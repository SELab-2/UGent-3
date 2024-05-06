"use strict";(self.webpackChunkdocumentation=self.webpackChunkdocumentation||[]).push([[827],{9674:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>u,contentTitle:()=>o,default:()=>d,frontMatter:()=>a,metadata:()=>i,toc:()=>l});var r=n(4848),s=n(8453);const a={},o="Python evaluator",i={id:"evaluators/python_evaluator",title:"Python evaluator",description:"General usage",source:"@site/i18n/nl/docusaurus-plugin-content-docs/current/evaluators/python_evaluator.md",sourceDirName:"evaluators",slug:"/evaluators/python_evaluator",permalink:"/nl/docs/evaluators/python_evaluator",draft:!1,unlisted:!1,editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/evaluators/python_evaluator.md",tags:[],version:"current",frontMatter:{},sidebar:"tutorialSidebar",previous:{title:"General evaluator",permalink:"/nl/docs/evaluators/general_evaluator"},next:{title:"Project upload form",permalink:"/nl/docs/category/project-upload-form"}},u={},l=[{value:"General usage",id:"general-usage",level:2},{value:"Structure",id:"structure",level:2},{value:"Running tests",id:"running-tests",level:2}];function c(e){const t={code:"code",h1:"h1",h2:"h2",p:"p",...(0,s.R)(),...e.components};return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(t.h1,{id:"python-evaluator",children:"Python evaluator"}),"\n",(0,r.jsx)(t.h2,{id:"general-usage",children:"General usage"}),"\n",(0,r.jsx)(t.p,{children:"This evaluator is responsible for running and executing tests on a student's Python code."}),"\n",(0,r.jsx)(t.h2,{id:"structure",children:"Structure"}),"\n",(0,r.jsxs)(t.p,{children:["When submitting the project a teacher can add a requirements manifest ",(0,r.jsx)(t.code,{children:"req-manifest.txt"}),", this way only the packages in the requirements file are usable on the evaluator."]}),"\n",(0,r.jsxs)(t.p,{children:["When no manifest is present, students are able to install their own depedencies with a ",(0,r.jsx)(t.code,{children:"requirements.txt"})," and a ",(0,r.jsx)(t.code,{children:"dev-requirements.txt"}),".\nOr the teacher can add a ",(0,r.jsx)(t.code,{children:"requirements.txt"})," if they want to pre install dependencies that a are present for testing the project."]}),"\n",(0,r.jsx)(t.h2,{id:"running-tests",children:"Running tests"}),"\n",(0,r.jsxs)(t.p,{children:["When a ",(0,r.jsx)(t.code,{children:"run_tests.sh"})," is present in the project assignment files, it will be run when the student is submitting their code.\nWhen running tests, it's important to note that the root of the student's submission will be ",(0,r.jsx)(t.code,{children:"/submission"}),"."]})]})}function d(e={}){const{wrapper:t}={...(0,s.R)(),...e.components};return t?(0,r.jsx)(t,{...e,children:(0,r.jsx)(c,{...e})}):c(e)}},8453:(e,t,n)=>{n.d(t,{R:()=>o,x:()=>i});var r=n(6540);const s={},a=r.createContext(s);function o(e){const t=r.useContext(a);return r.useMemo((function(){return"function"==typeof e?e(t):{...t,...e}}),[t,e])}function i(e){let t;return t=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:o(e.components),r.createElement(a.Provider,{value:t},e.children)}}}]);