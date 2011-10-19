%define name urbanterror
%define oname UrbanTerror

%define version 4.1.1
%define oversion 411

%define release %mkrel 1

Summary: Urban Terror is a free multi-player first person shooter
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.iourt.com/files/%{oname}%{oversion}.zip
Source1: http://ftp.snt.utwente.nl/pub/games/urbanterror/iourbanterror/source/ioUrbanTerrorSource_2007_12_20.zip
Source10: %{name}-128.png
Source11: %{name}-64.png
Source12: %{name}-32.png
Source13: %{name}-16.png
Patch0: urbanterror-4.1.1-q3asm.patch
Patch1: urbanterror-4.1.1-libcurl.patch
Patch2: urbanterror-4.1.1-x86_64.patch
License: GPLv2+
Group: Games/Arcade
Url: http://urbanterror.info
BuildRequires: SDL-devel
BuildRequires: mesagl-devel
Requires: %{name}-data = %{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Urban Terror(TM) is a free multi-player first person shooter developed by 
FrozenSand, that (thanks to the ioquake3-code) does not require Quake III 
Arena anymore. It is available for Windows, Linux and Macintosh. 
The current version is 4.1.

Urban Terror can be described as a Hollywood tactical shooter; somewhat 
realism based, but the motto is "fun over realism". This results in a very 
unique, enjoyable and addictive game.

No registration required: Install&play!

%package -n %{name}-data
Summary: Urban Terror data files (graphics, music, maps etc)
Requires: %{name} = %{version}
Group: Games/Arcade
BuildArch: noarch

%description -n %{name}-data
Data files used to play Urban Terror.

%prep
%setup -q -n %{oname} -c -a 1
%patch0 -p0
%patch1 -p1
%patch2 -p1

%build
%__mkdir_p build
pushd ioUrbanTerrorClientSource
%make DEFAULT_BASEDIR=%{_gamesdatadir}/%{name} USE_CURL=1
cp build/*/ioUrbanTerror.* ../build/
pushd

pushd ioUrbanTerrorServerSource
%make DEFAULT_BASEDIR=%{_gamesdatadir}/%{name} USE_CURL=1
cp build/*/ioUrTded.* ../build/
pushd

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}%{_gamesbindir}
%__cp build/ioUrTded.* %{buildroot}%{_gamesbindir}/%{name}-server
%__cp build/ioUrbanTerror.* %{buildroot}%{_gamesbindir}/%{name}

%__install -d %{buildroot}%{_gamesdatadir}/%{name}
%__cp -r %{oname}/q3ut4 %{buildroot}%{_gamesdatadir}/%{name}/

%__install -D -m 644 %{SOURCE13} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%__install -D -m 644 %{SOURCE12} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%__install -D -m 644 %{SOURCE11} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%__install -D -m 644 %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%__install -d %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Urban Terror
Comment=%{summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;ArcadeGame;
EOF

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{oname}/*.txt
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-server
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%files -n %{name}-data
%defattr(-,root,root)
%dir %{_gamesdatadir}/%{name}/q3ut4
%{_gamesdatadir}/%{name}/q3ut4/*

