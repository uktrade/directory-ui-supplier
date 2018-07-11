'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const PROJECT_DIR = path.resolve(__dirname);
const CORE_IN = `${PROJECT_DIR}/core/static/core/sass/**/*.scss`;
const CORE_OUT = `${PROJECT_DIR}/core/static/core`;
const ENROLMENT_IN = `${PROJECT_DIR}/enrolment/static/sass/**/*.scss`;
const ENROLMENT_OUT = `${PROJECT_DIR}/enrolment/static`;
const INDUSTRY_IN = `${PROJECT_DIR}/industry/static/industry/sass/**/*.scss`;
const INDUSTRY_OUT = `${PROJECT_DIR}/industry/static/industry`;

gulp.task('sass:core', function () {
  return gulp.src(CORE_IN)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        './ui/',
        'node_modules/govuk_frontend_toolkit/stylesheets',
        'enrolment/static/sass',
        'core/static/core/sass',
        'node_modules/govuk-elements-sass/public/sass'
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(CORE_OUT));
});

gulp.task('sass:enrolment', function () {
  return gulp.src(ENROLMENT_IN)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        './ui/',
        'node_modules/govuk_frontend_toolkit/stylesheets',
        'enrolment/static/sass',
        'core/static/core/sass',
        'node_modules/govuk-elements-sass/public/sass'
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(ENROLMENT_OUT));
});

gulp.task('sass:industry', function () {
  return gulp.src(INDUSTRY_IN)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        './ui/',
        'node_modules/govuk_frontend_toolkit/stylesheets',
        'enrolment/static/sass',
        'core/static/core/sass',
        'node_modules/govuk-elements-sass/public/sass'
      ],
      outputStyle: 'compressed'
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('./maps'))
    .pipe(gulp.dest(INDUSTRY_OUT));
});

gulp.task('sass', ['sass:core', 'sass:enrolment', 'sass:industry']);

gulp.task('sass:watch', function () {
  gulp.watch([CORE_IN, ENROLMENT_IN, INDUSTRY_IN], ['sass']);
});

gulp.task('default', ['sass']);
