import numpy as np
import pygame as pg
import recorder

nl = "\n"
asciiArray = [
  "   .-."+nl+
  "  /   \\           .-.                                 .-."+nl+
  " /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------"+nl+
  "         \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "          \\   /         `-'                     `-'         \\   /"+nl+
  "           `-'                                               `-'",

  "    .-."+nl+
  "   /   \\           .-.                                 .-."+nl+
  "  /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "-/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\------"+nl+
  "/         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  "           \\   /         `-'                     `-'         \\   /"+nl+
  "            `-'                                               `-'",

  "     .-."+nl+
  "    /   \\           .-.                                 .-."+nl+
  "   /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "--/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-----"+nl+
  " /         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  "/           \\   /         `-'                     `-'         \\"+nl+
  "             `-'                                               `-'",

  "      .-."+nl+
  "     /   \\           .-.                                 .-."+nl+
  "    /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "---/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\----"+nl+
  "  /         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  " /           \\   /         `-'                     `-'         \\"+nl+
  "'             `-'                                               `-",

  "       .-."+nl+
  "      /   \\           .-.                                 .-."+nl+
  "     /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "----/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\---"+nl+
  "   /         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  "  /           \\   /         `-'                     `-'         \\"+nl+
  "-'             `-'                                               `",

  "        .-."+nl+
  "       /   \\           .-.                                 .-."+nl+
  "      /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "-----/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\--"+nl+
  "    /         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  "   /           \\   /         `-'                     `-'         \\"+nl+
  "`-'             `-'",

  "         .-."+nl+
  "        /   \\           .-.                                 .-."+nl+
  "       /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-"+nl+
  "     /         \\     /       \\   /     `-'   `-'     \\   /       \\"+nl+
  "\\   /           \\   /         `-'                     `-'"+nl+
  " `-'             `-'",

  "          .-."+nl+
  "         /   \\           .-.                                 .-."+nl+
  "        /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\"+nl+
  "\\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  " \\   /           \\   /         `-'                     `-'"+nl+
  "  `-'             `-'",

  "           .-."+nl+
  "          /   \\           .-.                                 .-."+nl+
  "         /     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----"+nl+
  " \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "  \\   /           \\   /         `-'                     `-'"+nl+
  "   `-'             `-'",

  "            .-."+nl+
  "           /   \\           .-.                                 .-."+nl+
  "\\         /     \\         /   \\       .-.     _     .-.       /"+nl+
  "-\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/----"+nl+
  "  \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "   \\   /           \\   /         `-'                     `-'"+nl+
  "    `-'             `-'",

  "             .-."+nl+
  ".           /   \\           .-.                                 .-"+nl+
  " \\         /     \\         /   \\       .-.     _     .-.       /"+nl+
  "--\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/---"+nl+
  "   \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "    \\   /           \\   /         `-'                     `-'"+nl+
  "     `-'             `-'",

  "              .-."+nl+
  "-.           /   \\           .-.                                 ."+nl+
  "  \\         /     \\         /   \\       .-.     _     .-.       /"+nl+
  "---\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/--"+nl+
  "    \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "     \\   /           \\   /         `-'                     `-'"+nl+
  "      `-'             `-'",

  "               .-."+nl+
  ".-.           /   \\           .-."+nl+
  "   \\         /     \\         /   \\       .-.     _     .-.       /"+nl+
  "----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-"+nl+
  "     \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "      \\   /           \\   /         `-'                     `-'"+nl+
  "       `-'             `-'",

  "                .-."+nl+
  " .-.           /   \\           .-."+nl+
  "/   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/"+nl+
  "      \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "       \\   /           \\   /         `-'                     `-'"+nl+
  "        `-'             `-'",

  "                 .-."+nl+
  "  .-.           /   \\           .-."+nl+
  " /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-----"+nl+
  "       \\     /         \\     /       \\   /     `-'   `-'     \\   /"+nl+
  "        \\   /           \\   /         `-'                     `-'"+nl+
  "         `-'             `-'",

  "                  .-."+nl+
  "   .-.           /   \\           .-."+nl+
  "  /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "-/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\----"+nl+
  "/       \\     /         \\     /       \\   /     `-'   `-'     \\"+nl+
  "         \\   /           \\   /         `-'                     `-'"+nl+
  "          `-'             `-'",

  "                   .-."+nl+
  "    .-.           /   \\           .-."+nl+
  "   /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "--/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\---"+nl+
  " /       \\     /         \\     /       \\   /     `-'   `-'     \\"+nl+
  "'         \\   /           \\   /         `-'                     `-"+nl+
  "           `-'             `-'",

  "                    .-."+nl+
  "     .-.           /   \\           .-."+nl+
  "    /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "---/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\--"+nl+
  "  /       \\     /         \\     /       \\   /     `-'   `-'     \\"+nl+
  "-'         \\   /           \\   /         `-'                     `"+nl+
  "            `-'             `-'",

  "                     .-."+nl+
  "      .-.           /   \\           .-."+nl+
  "     /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\-"+nl+
  "   /       \\     /         \\     /       \\   /     `-'   `-'     \\"+nl+
  "`-'         \\   /           \\   /         `-'"+nl+
  "             `-'             `-'",

  "                      .-."+nl+
  "       .-.           /   \\           .-."+nl+
  "      /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---\\"+nl+
  "\\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  " `-'         \\   /           \\   /         `-'"+nl+
  "              `-'             `-'",

  "                       .-."+nl+
  "        .-.           /   \\           .-."+nl+
  "       /   \\         /     \\         /   \\       .-.     _     .-."+nl+
  "\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/---"+nl+
  " \\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  "  `-'         \\   /           \\   /         `-'"+nl+
  "               `-'             `-'",

  "                        .-."+nl+
  "         .-.           /   \\           .-."+nl+
  ".       /   \\         /     \\         /   \\       .-.     _     .-"+nl+
  "-\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/--"+nl+
  "  \\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  "   `-'         \\   /           \\   /         `-'"+nl+
  "                `-'             `-'",

  "                         .-."+nl+
  "          .-.           /   \\           .-."+nl+
  "-.       /   \\         /     \\         /   \\       .-.     _     ."+nl+
  "--\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/-"+nl+
  "   \\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  "    `-'         \\   /           \\   /         `-'"+nl+
  "                 `-'             `-'",

  "                          .-."+nl+
  "           .-.           /   \\           .-."+nl+
  ".-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---/"+nl+
  "    \\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  "     `-'         \\   /           \\   /         `-'"+nl+
  "                  `-'             `-'",

  "                           .-."+nl+
  "            .-.           /   \\           .-."+nl+
  " .-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\---"+nl+
  "     \\   /       \\     /         \\     /       \\   /     `-'   `-'"+nl+
  "      `-'         \\   /           \\   /         `-'"+nl+
  "                   `-'             `-'",

  "                            .-."+nl+
  "             .-.           /   \\           .-."+nl+
  "  .-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "-/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\--"+nl+
  "'     \\   /       \\     /         \\     /       \\   /     `-'   `-"+nl+
  "       `-'         \\   /           \\   /         `-'"+nl+
  "                    `-'             `-'",

  "                             .-."+nl+
  "              .-.           /   \\           .-."+nl+
  "   .-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "--/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\-"+nl+
  "-'     \\   /       \\     /         \\     /       \\   /     `-'   `"+nl+
  "        `-'         \\   /           \\   /         `-'"+nl+
  "                     `-'             `-'",

  "                              .-."+nl+
  "               .-.           /   \\           .-."+nl+
  "    .-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-\\"+nl+
  "`-'     \\   /       \\     /         \\     /       \\   /     `-'"+nl+
  "         `-'         \\   /           \\   /         `-'"+nl+
  "                      `-'             `-'",

  "                               .-."+nl+
  "                .-.           /   \\           .-."+nl+
  "     .-.       /   \\         /     \\         /   \\       .-.     _"+nl+
  "\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/-"+nl+
  " `-'     \\   /       \\     /         \\     /       \\   /     `-'"+nl+
  "          `-'         \\   /           \\   /         `-'"+nl+
  "                       `-'             `-'",

  "                                .-."+nl+
  "                 .-.           /   \\           .-."+nl+
  "_     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---/"+nl+
  "  `-'     \\   /       \\     /         \\     /       \\   /     `-'"+nl+
  "           `-'         \\   /           \\   /         `-'"+nl+
  "                        `-'             `-'",

  "                                 .-."+nl+
  "                  .-.           /   \\           .-."+nl+
  " _     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\---"+nl+
  "   `-'     \\   /       \\     /         \\     /       \\   /     `-'"+nl+
  "            `-'         \\   /           \\   /         `-'"+nl+
  "                         `-'             `-'",

  "                                  .-."+nl+
  "                   .-.           /   \\           .-."+nl+
  "  _     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "-/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\--"+nl+
  "'   `-'     \\   /       \\     /         \\     /       \\   /     `-"+nl+
  "             `-'         \\   /           \\   /         `-'"+nl+
  "                          `-'             `-'",

  "                                   .-."+nl+
  "                    .-.           /   \\           .-."+nl+
  "   _     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "--/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\-"+nl+
  "-'   `-'     \\   /       \\     /         \\     /       \\   /     `"+nl+
  "              `-'         \\   /           \\   /         `-'"+nl+
  "                           `-'             `-'",

  "                                    .-."+nl+
  "                     .-.           /   \\           .-."+nl+
  "    _     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---\\"+nl+
  "`-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "               `-'         \\   /           \\   /         `-'"+nl+
  "                            `-'             `-'",

  "                                     .-."+nl+
  "                      .-.           /   \\           .-."+nl+
  "     _     .-.       /   \\         /     \\         /   \\       .-."+nl+
  "\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/---"+nl+
  " `-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "                `-'         \\   /           \\   /         `-'"+nl+
  "                            `-'             `-'",

  "                                      .-."+nl+
  "                       .-.           /   \\           .-."+nl+
  ".     _     .-.       /   \\         /     \\         /   \\       .-"+nl+
  "-\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/--"+nl+
  "  `-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "                 `-'         \\   /           \\   /         `-'"+nl+
  "                              `-'             `-'",

  "                                       .-."+nl+
  "                        .-.           /   \\           .-."+nl+
  "-.     _     .-.       /   \\         /     \\         /   \\       ."+nl+
  "--\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/-"+nl+
  "   `-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "                  `-'         \\   /           \\   /         `-'"+nl+
  "                               `-'             `-'",

  "                                        .-."+nl+
  "                         .-.           /   \\           .-."+nl+
  ".-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----/"+nl+
  "    `-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "                   `-'         \\   /           \\   /         `-'"+nl+
  "                                `-'             `-'",

  "                                         .-."+nl+
  "                          .-.           /   \\           .-."+nl+
  " .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-----"+nl+
  "     `-'   `-'     \\   /       \\     /         \\     /       \\   /"+nl+
  "                    `-'         \\   /           \\   /         `-'"+nl+
  "                                 `-'             `-'",

  "                                          .-."+nl+
  "                           .-.           /   \\           .-."+nl+
  "  .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "-/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\----"+nl+
  "/     `-'   `-'     \\   /       \\     /         \\     /       \\"+nl+
  "                     `-'         \\   /           \\   /         `-'"+nl+
  "                                  `-'             `-'",

  "                                           .-."+nl+
  "                            .-.           /   \\           .-."+nl+
  "   .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "--/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\---"+nl+
  " /     `-'   `-'     \\   /       \\     /         \\     /       \\"+nl+
  "'                     `-'         \\   /           \\   /         `-"+nl+
  "                                   `-'             `-'",

  "                                            .-."+nl+
  "                             .-.           /   \\           .-."+nl+
  "    .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "---/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\--"+nl+
  "  /     `-'   `-'     \\   /       \\     /         \\     /       \\"+nl+
  "-'                     `-'         \\   /           \\   /         `"+nl+
  "                                    `-'             `-'",

  "                                             .-."+nl+
  "                              .-.           /   \\           .-."+nl+
  "     .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\-"+nl+
  "   /     `-'   `-'     \\   /       \\     /         \\     /       \\"+nl+
  "`-'                     `-'         \\   /           \\   /"+nl+
  "                                     `-'             `-'",

  "                                              .-."+nl+
  "                               .-.           /   \\           .-."+nl+
  "      .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----\\"+nl+
  "\\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  " `-'                     `-'         \\   /           \\   /"+nl+
  "                                      `-'             `-'",

  "                                               .-."+nl+
  "                                .-.           /   \\           .-."+nl+
  "       .-.     _     .-.       /   \\         /     \\         /   \\"+nl+
  "\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-----"+nl+
  " \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "  `-'                     `-'         \\   /           \\   /"+nl+
  "                                       `-'             `-'",

  "                                                .-."+nl+
  "                                 .-.           /   \\           .-."+nl+
  "\\       .-.     _     .-.       /   \\         /     \\         /"+nl+
  "-\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/----"+nl+
  "  \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "   `-'                     `-'         \\   /           \\   /"+nl+
  "                                        `-'             `-'",

  "                                                 .-."+nl+
  ".                                 .-.           /   \\           .-"+nl+
  " \\       .-.     _     .-.       /   \\         /     \\         /"+nl+
  "--\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/---"+nl+
  "   \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "    `-'                     `-'         \\   /           \\   /"+nl+
  "                                         `-'             `-'",

  "                                                  .-."+nl+
  "-.                                 .-.           /   \\           ."+nl+
  "  \\       .-.     _     .-.       /   \\         /     \\         /"+nl+
  "---\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/--"+nl+
  "    \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "     `-'                     `-'         \\   /           \\   /"+nl+
  "                                          `-'             `-'",

  "                                                   .-."+nl+
  ".-.                                 .-.           /   \\"+nl+
  "   \\       .-.     _     .-.       /   \\         /     \\         /"+nl+
  "----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/-"+nl+
  "     \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "      `-'                     `-'         \\   /           \\   /"+nl+
  "                                           `-'             `-'",

  "                                                    .-."+nl+
  " .-.                                 .-.           /   \\"+nl+
  "/   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------/"+nl+
  "      \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "       `-'                     `-'         \\   /           \\   /"+nl+
  "                                            `-'             `-'",

  "                                                     .-."+nl+
  "  .-.                                 .-.           /   \\"+nl+
  " /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-------"+nl+
  "       \\   /     `-'   `-'     \\   /       \\     /         \\     /"+nl+
  "        `-'                     `-'         \\   /           \\   /"+nl+
  "                                             `-'             `-'",

  "                                                      .-."+nl+
  "   .-.                                 .-.           /   \\"+nl+
  "  /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "-/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\------"+nl+
  "/       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  "         `-'                     `-'         \\   /           \\   /"+nl+
  "                                              `-'             `-'",

  "                                                       .-."+nl+
  "    .-.                                 .-.           /   \\"+nl+
  "   /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "--/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-----"+nl+
  " /       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  "/         `-'                     `-'         \\   /           \\"+nl+
  "                                               `-'             `-'",

  "                                                        .-."+nl+
  "     .-.                                 .-.           /   \\"+nl+
  "    /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "---/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\----"+nl+
  "  /       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  " /         `-'                     `-'         \\   /           \\"+nl+
  "'                                               `-'             `-",

  "                                                         .-."+nl+
  "      .-.                                 .-.           /   \\"+nl+
  "     /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "----/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\---"+nl+
  "   /       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  "  /         `-'                     `-'         \\   /           \\"+nl+
  "-'                                               `-'             `",

  "                                                          .-."+nl+
  "       .-.                                 .-.           /   \\"+nl+
  "      /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "-----/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\--"+nl+
  "    /       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  "   /         `-'                     `-'         \\   /           \\"+nl+
  "`-'                                               `-'",

  "                                                           .-."+nl+
  "        .-.                                 .-.           /   \\"+nl+
  "       /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\-"+nl+
  "     /       \\   /     `-'   `-'     \\   /       \\     /         \\"+nl+
  "\\   /         `-'                     `-'         \\   /"+nl+
  " `-'                                               `-'",

  "                                                            .-."+nl+
  "         .-.                                 .-.           /   \\"+nl+
  "        /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------\\"+nl+
  "\\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  " \\   /         `-'                     `-'         \\   /"+nl+
  "  `-'                                               `-'",

  "                                                             .-."+nl+
  "          .-.                                 .-.           /   \\"+nl+
  "         /   \\       .-.     _     .-.       /   \\         /     \\"+nl+
  "\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-------"+nl+
  " \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "  \\   /         `-'                     `-'         \\   /"+nl+
  "   `-'                                               `-'",

  "                                                              .-."+nl+
  "           .-.                                 .-.           /   \\"+nl+
  "\\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "-\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/------"+nl+
  "  \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "   \\   /         `-'                     `-'         \\   /"+nl+
  "    `-'                                               `-'",

  "                                                               .-."+nl+
  "\\           .-.                                 .-.           /"+nl+
  " \\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "--\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-----"+nl+
  "   \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "    \\   /         `-'                     `-'         \\   /"+nl+
  "     `-'                                               `-'",

  ".                                                               .-"+nl+
  " \\           .-.                                 .-.           /"+nl+
  "  \\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "---\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/----"+nl+
  "    \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "     \\   /         `-'                     `-'         \\   /"+nl+
  "      `-'                                               `-'",

  "-.                                                               ."+nl+
  "  \\           .-.                                 .-.           /"+nl+
  "   \\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "----\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/---"+nl+
  "     \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "      \\   /         `-'                     `-'         \\   /"+nl+
  "       `-'                                               `-'",

  ".-."+nl+
  "   \\           .-.                                 .-.           /"+nl+
  "    \\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "-----\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/--"+nl+
  "      \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "       \\   /         `-'                     `-'         \\   /"+nl+
  "        `-'                                               `-'",

  " .-."+nl+
  "/   \\           .-.                                 .-."+nl+
  "     \\         /   \\       .-.     _     .-.       /   \\         /"+nl+
  "------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/-"+nl+
  "       \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "        \\   /         `-'                     `-'         \\   /"+nl+
  "         `-'                                               `-'",

  "  .-."+nl+
  " /   \\           .-.                                 .-."+nl+
  "/     \\         /   \\       .-.     _     .-.       /   \\"+nl+
  "-------\\-------/-----\\-----/---\\---/-\\---/---\\-----/-----\\-------/"+nl+
  "        \\     /       \\   /     `-'   `-'     \\   /       \\     /"+nl+
  "         \\   /         `-'                     `-'         \\   /"+nl+
  "          `-'                                               `-'"]

class SineSound:
  """SineSound"""
  def __init__(self, frequency=300, gain=0.1, samplerate=44100, channels=1, bits=16, amplitude=1.0):
    self.freq = frequency
    self.gain = gain
    self.amplitude = amplitude
    self.samplerate = samplerate
    self.channels = channels
    self.bits = bits
    self.sound = None    
    pg.mixer.pre_init(self.samplerate, -self.bits, self.channels)
    pg.init()
    self.channel = pg.mixer.Channel(0)
    self.channel.set_volume(1.0)
    self._recording = False
    self.recorder = None
    self.ascii = asciiArray

  def start(self):
    if self.sound == None:
      self.sound = self.mkSine(self.freq, self.amplitude, self.samplerate, self.channels)
    #self.sound.play(-1)
    self.channel.play(self.sound, -1)

  def change(self, frequency=300, amplitude=1.0):
    self.freq = frequency
    self.amplitude = amplitude
    newSound = self.mkSine(self.freq, self.amplitude, self.samplerate, self.channels)
    #pg.mixer.stop()
    # self.channel.queue(newSound)
    self.channel.play(newSound, -1)
    self.sound.stop()
    self.sound = newSound
    #self.sound.play(-1)

  def mkSine(self, freq=1000, peak=1.0, samplerate=44100, nchannels=1):
    wavelen = 0.0
    if( freq != 0.0 ):
      wavelen = 1.0/freq
    wavesize = wavelen * samplerate

    sinusoid = (2**15 - 1) * np.sin(2.0 * np.pi * freq * np.arange(0, wavesize) / float(samplerate)) * peak
    samples = np.array(sinusoid, dtype=np.int16)
    if(nchannels > 1):
      samples = np.tile(samples, (nchannels, 1)).T

    sound = pg.sndarray.make_sound(samples)
    sound.set_volume(self.gain)
    # print 'set to freq: %.2f, gain: %.2f' % (freq, self.gain)
    return sound


  def setGain(self, gain):
    self.gain = gain
    if self.sound != None:
      self.sound.set_volume(gain)

  def record(self):
    self._recording = True

  def recording(self):
    return self._recording

  def loadFile(self, path):
    self.sound = pg.mixer.Sound(path)

  def playOnce(self, path=None):
    if(path != None):
      self.loadFile(path)
    self.sound.play()



class FileSound:
  def __init__(self, path=None, gain=0.3, verbose=False):
    self.verbose = verbose
    self.path = path
    self.sound = None
    self.channel = pg.mixer.Channel(1)
    self.gain = gain
    if(self.path != None):
      self.loadFile(self.path)

  def loadFile(self, fPath):
    self.sound = pg.mixer.Sound(fPath)

  def play(self, restart=False):
    if(self.isPlaying() and restart != True):
      return
    self.channel.play(self.sound)   
    #self.sound.play() # default: once

  def stop(self):
    if self.channel.get_busy():
      self.log('FileSound: stopping')

    self.channel.stop()

  def isPlaying(self):
    # if(self.sound == None):
    #  return False
    return self.channel.get_busy() #pg.mixer.get_busy()

  def log(self, msg):
    if self.verbose:
      print(msg)
