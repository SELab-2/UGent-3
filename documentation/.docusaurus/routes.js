import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '333'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', 'e60'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '383'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', '8c9'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'eba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '94d'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', 'a0c'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '701'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'ac1'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'f97'),
            routes: [
              {
                path: '/docs/category/evaluators',
                component: ComponentCreator('/docs/category/evaluators', 'f11'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/category/project-upload-form',
                component: ComponentCreator('/docs/category/project-upload-form', '8a1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/evaluators/custom_evaluator',
                component: ComponentCreator('/docs/evaluators/custom_evaluator', '6e4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/evaluators/general_evaluator',
                component: ComponentCreator('/docs/evaluators/general_evaluator', '87d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/evaluators/python_evaluator',
                component: ComponentCreator('/docs/evaluators/python_evaluator', '425'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/projectform/project_upload_form',
                component: ComponentCreator('/docs/projectform/project_upload_form', 'ace'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '449'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
