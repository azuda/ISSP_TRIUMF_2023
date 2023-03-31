Installing the povlinux binary package is fairly easy but in case you are new to GNU/Linux or POV-Ray you might find this tutorial useful.

This tutorial is exclusively for Users of x86 PCs running GNU/Linux. If you have different hardware or run a different OS you need a different package from the Download page.

This tutorial only covers the system level installation that requires root privileges. If you don't have them you can still install the binary distribution but this is not completely covered by this tutorial. To do this follow steps 1 to 7 below and then run the install script as normal user.

   1. Open a shell
   2.

      create a temporary directory somewhere to unpack the POV-Ray distribution
      for example:

user@machine:~> mkdir ~/povray/

   3.

      Get the POV-Ray for GNU/Linux binary package from the POV-Ray website
      This can be done by right clicking on the following link and choosing 'Save Link As.../Save Link Target As...':

      Download povlinux-3.6.tgz binary distribution

      Save this package in the new directory you just created, for example /home/<username>/povray/.
   4. switch back to the shell
   5.

      change into the directory where you just saved the package:
      for example

user@machine:~> cd ~/povray/

   6.

      unpack the distribution:

user@machine:~/povray> tar xvfz povlinux.tgz

      you should get a long listing of all files extracted from the package.
   7.

      change into the distribution directory:

user@machine:~/povray> cd povray-3.6

   8.

      become root:

user@machine:~/povray/povray-3.6> su
Password: <enter root password>

   9.

      run the install script:

root@machine:/home/user/povray/povray-3.6> ./install

      If you previously had no other POV-Ray version installed the installation should run without interruptions. Otherwise there might be additional decisions required.

      Check if the install script reports any problems. At the end you will be asked if you want to do a test render. This test render will be without display when run as root.
  10.

      leave the root environment:

root@machine:/home/user/povray/povray-3.6> exit

  11.

      if you had previously installed POV-Ray
      or if you want to be able to customize your configuration independently from other users:

user@machine:~/povray/povray-3.6 > ./install user

      This will update the user configuration files in ~/.povray/3.6/.
  12.

      if you are using KDE:

user@machine:~/povray/povray-3.6> ./install kde

      This installs some useful entries in the KDE panel and registers POV-Ray file types.
  13.

      to test if installation was successful
      you can run a short test render:

user@machine:~/povray/povray-3.6> ./install test

      If this fails there probably was some problem during the install that required manual action. Check the messages printed by the install script and try to run the install again.

That was it!

You can render the sample scenes and animations coming with POV-Ray. When you are using KDE you can do this with the corresponding links in the KDE panel, otherwise you can call the sample scene render scripts manually - this is explained in the documentation.

After a successful installation the documentation can be found in /usr/local/share/doc/povray-3.6/html/.
