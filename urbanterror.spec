%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define oname UrbanTerror
%define oversion 42
%define majver 4.2
%define minver 014

Summary:	Urban Terror is a free multi-player first person shooter
Name:		urbanterror
Version:	%{majver}.%{minver}
Release:	3
License:	GPLv2+
Group:		Games/Arcade
Url:		http://urbanterror.info
Source0:	http://cdn.urbanterror.info/urt/%{oversion}/zips/%{oname}%{oversion}_full%{minver}.zip
Source1:	https://github.com/Barbatos/ioq3-for-%{oname}-4/archive/ioq3-for-%{oname}-4-release-%{version}.tar.gz
Source10:	%{name}-128.png
Source11:	%{name}-64.png
Source12:	%{name}-32.png
Source13:	%{name}-16.png
Patch0:		urbanterror-4.2.014-q3asm.patch
Patch1:		urbanterror-4.2.014-libcurl.patch
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(vorbisfile)
Requires:	%{name}-data = %{version}

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
Summary:	Urban Terror data files (graphics, music, maps etc)
Requires:	%{name} = %{version}
Group:		Games/Arcade
License:	Freeware
BuildArch:	noarch

%description -n %{name}-data
Data files used to play Urban Terror.

Warning! Read the license for data files carefully.

"Urban Terror is distributed free over the Internet and is covered by the
Quake 3 SDK licence agreement. The mod files may not be sold [in any form]
or distributed on physical media unless with permission from iD Software."

%prep
%setup -q -n %{oname} -c -a 1
%patch0 -p0
%patch1 -p0

%build
mkdir -p build
pushd ioq3-for-%{oname}-4-release-%{version}
%make \
	DEFAULT_BASEDIR=%{_gamesdatadir}/%{name} \
	USE_CURL=1 \
	USE_OPENAL=1 \
	USE_CODEC_VORBIS=1 \
	BUILD_CLIENT=1 \
	BUILD_SERVER=1
cp build/*/*-UrT.* ../build/
cp build/*/*-UrT-Ded.* ../build/
popd

%install
install -d %{buildroot}%{_gamesbindir}
cp build/*-UrT-Ded.* %{buildroot}%{_gamesbindir}/%{name}-server
cp build/*-UrT.* %{buildroot}%{_gamesbindir}/%{name}

install -d %{buildroot}%{_gamesdatadir}/%{name}
cp -r %{oname}%{oversion}/q3ut4 %{buildroot}%{_gamesdatadir}/%{name}/

install -D -m 644 %{SOURCE13} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -D -m 644 %{SOURCE12} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -D -m 644 %{SOURCE11} %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D -m 644 %{SOURCE10} %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

install -d %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

%files
%doc %{oname}%{oversion}/q3ut4/*.txt %{oname}%{oversion}/q3ut4/*.doc
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-server
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_iconsdir}/hicolor/128x128/apps/%{name}.png

%files -n %{name}-data
%dir %{_gamesdatadir}/%{name}/q3ut4
%{_gamesdatadir}/%{name}/q3ut4/*

