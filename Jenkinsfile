#!groovy

@Library('shared-library') _
import quarticpipeline.PipelineBuilder

containerNodes = [
  Publish: [
    dir: './jenkins-scripts/',
    steps: [
      publish: [
        file_name: 'publish.sh',
      ]
    ]
  ]
]

pipelineBuilder = new PipelineBuilder(this, env, scm, containerNodes)
userEnv = ['RESERVE=azubuntu','MAKE_OBFUSCATE=true','OBFUSCATE_DIR=../djangosaml2-obfuscated']

pipelineBuilder.executePipeline(userEnv)
